# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import xlrd
import xlwt
from datetime import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from coop.models import Collection, CooperativeMember
from coop.forms import CollectionForm, CollectionFilterForm
from coop.views.member import save_transaction
from coop.utils import credit_member_account, debit_member_account
from conf.utils import generate_alpanumeric, genetate_uuid4, log_error, get_message_template as message_template
from coop.utils import sendMemberSMS
from credit.utils import check_loan, pay_loan


class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_collection']
        context.update(self.extra_context)
        return context


class CollectionListView(ExtraContext, ListView):
    model = Collection
    ordering = ['-create_date']
    extra_context = {'active': ['_collection']}
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.GET.get('_download'):
            return redirect('coop:collection_download')
        else:
            return super(CollectionListView, self).dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        queryset = super(CollectionListView, self).get_queryset()
        
        if not self.request.user.profile.is_union():
            if not self.request.user.profile.is_partner():
                if hasattr(self.request.user, 'cooperative_admin'):
                    cooperative = self.request.user.cooperative_admin.cooperative
                    queryset = queryset.filter(Q(member__cooperative=cooperative)| Q(cooperative=cooperative))
        search = self.request.GET.get('search')
        product = self.request.GET.get('product')
        cooperative = self.request.GET.get('cooperative')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        if search:
            queryset = queryset.filter(Q(member__first_name__icontains=search)|Q(member__surname__icontains=search)|Q(member__phone_number__icontains=search)|Q(member__member_id__icontains=search))
        if product:
            queryset = queryset.filter(product__id = product)
        if cooperative:
            queryset = queryset.filter(cooperative__id = cooperative)
        if start_date and end_date:
            queryset = queryset.filter(collection_date__gte = start_date, collection_date__lte = end_date)
        if start_date:
            queryset = queryset.filter(collection_date = start_date)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(CollectionListView, self).get_context_data(**kwargs)
        context['form'] = CollectionFilterForm(self.request.GET)
        return context


class CollectionDownload(View):
    def get(self, request, *args, **kwargs):
        columns = []
        fields = ['id', 'is_member', 'cooperative__name', 'member__surname', 'member__first_name', 'member__phone_number', 'collection_reference', 'product__name', 'quantity',
                               'unit_price', 'total_price', 'created_by']
        columns = [self.replaceMultiple(c, ['_', '__name'], ' ').title() for c in fields]
        
        #Gather the Information Found
        # Create the HttpResponse object with Excel header.This tells browsers that 
        # the document is a Excel file.
        response = HttpResponse(content_type='application/ms-excel')
        
        # The response also has additional Content-Disposition header, which contains 
        # the name of the Excel file.
        response['Content-Disposition'] = 'attachment; filename=CollectionLogs_%s.xls' % datetime.now().strftime('%Y%m%d%H%M%S')
        
        # Create object for the Workbook which is under xlwt library.
        workbook = xlwt.Workbook()
        
        # By using Workbook object, add the sheet with the name of your choice.
        worksheet = workbook.add_sheet("Collections")

        row_num = 0
        style_string = "font: bold on; borders: bottom dashed"
        style = xlwt.easyxf(style_string)

        for col_num in range(len(columns)):
            # For each cell in your Excel Sheet, call write function by passing row number, 
            # column number and cell data.
            worksheet.write(row_num, col_num, columns[col_num], style=style)
        
        _collection = Collection.objects.values(*fields).all()
        for m in _collection:
            row_num += 1
            row = [m['%s' % x] for x in fields]
            for col_num in range(len(row)):
                worksheet.write(row_num, col_num, row[col_num])
        workbook.save(response)
        return response
     
    def replaceMultiple(self, mainString, toBeReplaces, newString):
        # Iterate over the strings to be replaced
        for elem in toBeReplaces :
            # Check if string is in the main string
            if elem in mainString :
                # Replace the string
                mainString = mainString.replace(elem, newString)
        
        return  mainString       

    
class CollectionCreateView(ExtraContext, CreateView):
    model = Collection
    extra_context = {'active': ['_collection']}
    form_class = CollectionForm
    success_url = reverse_lazy('coop:collection_list')
    
    def get_form_kwargs(self):
        kwargs = super(CollectionCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs
    
    def form_valid(self, form):
        form.instance.collection_reference = genetate_uuid4()
        form.instance.created_by = self.request.user
        #form.instance.cooperative = self.request.user.cooperative_admin.cooperative
        
        if form.instance.is_member:
            params = {'amount': form.instance.total_price,
                      'member': form.instance.member,
                      'transaction_reference': form.instance.collection_reference ,
                      'transaction_category': 'COLLECTION',
                      'entry_type': 'CREDIT'
                      }
            member = CooperativeMember.objects.filter(pk=form.instance.member.id)
            if member.exists():
                member = member[0]
                qty_bal = member.collection_quantity if member.collection_quantity else 0
                
                new_bal = form.instance.quantity + qty_bal
                member.collection_quantity = new_bal
                member.save()
                # save_transaction(params)
                credit_member_account(params)

                loan = check_loan(member)
                if loan:
                    ploan = {
                        "member": form.instance.total_price,
                        "amount": form.instance.member,
                        "transaction_type": "LOAN REPAYMENT",
                        "created_by": "SYSTEM"
                    }

                    pay_loan(ploan)

                    params = {'amount': form.instance.total_price,
                              'member': form.instance.member,
                              'transaction_reference': form.instance.collection_reference,
                              'transaction_category': 'LOAN REPAYMENT',
                              'entry_type': 'DEBIT'
                              }
                    debit_member_account(params)
            
            try:
                message = message_template().collection
                message = message.replace('<NAME>', member.surname)
                message = message.replace('<QTY>', "%s%s" % (form.instance.quantity, form.instance.product.unit.code))
                message = message.replace('<PRODUCT>', "%s" % (form.instance.product.name))
                message = message.replace('<COOP>', form.instance.cooperative.name)
                message = message.replace('<DATE>', form.instance.collection_date.strftime('%Y-%m-%d'))
                message = message.replace('<AMOUNT>', "%s" % form.instance.total_price)
                message = message.replace('<REFNO>', form.instance.collection_reference)
                sendMemberSMS(self.request, member, message)
            except Exception:
                log_error()
        member = super(CollectionCreateView, self).form_valid(form)
        return member
      
    
class CollectionUpdateView(UpdateView):
    model = Collection
    form_class = CollectionForm
    extra_context = {'active': ['_collection', '__createcc']}
    success_url = reverse_lazy('activity:collection_create')
    
    def form_valid(self, form):
        form.instance.collection_reference = genetate_uuid4()
        return super(CollectionUpdateView, self).form_valid(form)
