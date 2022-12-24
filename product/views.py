# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import xlrd
import xlwt
import json
from django.utils.encoding import smart_str
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.forms.formsets import formset_factory, BaseFormSet
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db import transaction

from django.contrib.auth.models import User, Group

from conf.utils import log_debug, log_error
from product.models import *
from product.forms import *
from userprofile.models import Profile, AccessLevel
from product.api.fanumera import FamuneraAPI


class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_union_prod']
        context['title'] = 'Country'
        context.update(self.extra_context)
        return context
    

class ProductUnitListView(ExtraContext, ListView):
    model = ProductUnit
    
    def get_context_data(self, **kwargs):
        context = super(ProductUnitListView, self).get_context_data(**kwargs)
        context['active'].append('__unit')
        return context


class ProductUnitCreateView(ExtraContext, CreateView):
    model = ProductUnit
    form_class = ProductUnitForm
    template_name = "product/productunit_form.html"
    success_url = reverse_lazy('product:unit_list')
    # 
    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super(ProductCreateView, self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ProductUnitCreateView, self).get_context_data(**kwargs)
        context['active'].append('__unit')
        return context
    

class ProductUnitUpdateView(ExtraContext, UpdateView):
    model = ProductUnit
    form_class = ProductUnitForm
    template_name = "product/productunit_form.html"
    success_url = reverse_lazy('product:unit_list')
    # 
    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super(ProductUpdateView, self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ProductUnitUpdateView, self).get_context_data(**kwargs)
        context['active'].append('__unit')
        return context
    
    
class ProductVariationListView(ExtraContext, ListView):
    model = Product
    template_name = "product/productvariation_list.html"
    
    def get_context_data(self, **kwargs):
        context = super(ProductVariationListView, self).get_context_data(**kwargs)
        context['active'].append('__product')
        return context
    
    
class ProductVariationView(View):
    template_name = "product/product_variation_form.html"
    
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        prod = None
        var = None
        initial = None
        extra=1
        try:
            if pk:
                extra = 0
                prod = Product.objects.get(pk=pk)
                pvars = ProductVariation.objects.filter(product=prod)
                initial = [{'name': x.name, 'unit': x.unit} for x in pvars]
        except Exception as e:
            log_error()
            return redirect('product:variation_list')
        product_form = ProductForm(instance=prod)
        variation_form = formset_factory(ProductVariationForm, formset=BaseFormSet, extra=extra)
        variation_formset = variation_form(prefix='variation', initial=initial)
        data = {'form': product_form,
                'variation_formset': variation_formset,
                'active': ['_union_prod', '__product']}
        return render(request, self.template_name, data)
    
    def post(self, request, *args, **kwargs ):
        pk = self.kwargs.get('pk')
        prod = None
        var = None
        initial = None
        extra=1
        try:
            if pk:
                extra=1
                prod = Product.objects.get(pk=pk)
                pvars = ProductVariation.objects.filter(product=prod)
                initial = [{'name': x.name, 'unit': x.unit} for x in pvars]
        except Exception as e:
            log_error()
            return redirect('product:variation_list')
        product_form = ProductForm(request.POST, instance=prod)
        variation_form = formset_factory(ProductVariationForm, formset=BaseFormSet, extra=extra)
        variation_formset = variation_form(request.POST, prefix='variation')
        if product_form.is_valid() and variation_formset.is_valid():
            try:
                with transaction.atomic():
                    p = product_form.save(commit=False)
                    p.created_by = request.user
                    p.save()
                    if pk:
                        ProductVariation.objects.filter(product=p).delete()
                    for variation_form in variation_formset:
                        v = variation_form.save(commit=False)
                        v.product = p
                        v.created_by = request.user
                        v.save()
                return redirect('product:variation_list')
            except Exception as e:
                log_error()
        data = {'form': product_form,
                'variation_formset': variation_formset,
                'active': ['_union_prod', '__product']}
        return render(request, self.template_name, data)

# Variation Price
class ProductVariationPriceCreateView(ExtraContext, CreateView):
    model = ProductVariationPrice
    form_class = ProductVariationPriceForm
    template_name = "product/productvariationprice_form.html"
    success_url = reverse_lazy('product:price_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(ProductVariationPriceCreateView, self).form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super(ProductVariationPriceCreateView, self).get_context_data(**kwargs)
        context['active'].append('__price')
        return context
    

class ProductVariationPriceUpdateView(ExtraContext, UpdateView):
    model = ProductVariationPrice
    form_class = ProductVariationPriceForm
    template_name = "product/productvariationprice_form.html"
    success_url = reverse_lazy('product:price_list')
    # 
    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user
    #     return super(ProductUpdateView, self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(ProductVariationPriceUpdateView, self).get_context_data(**kwargs)
        context['active'].append('__price')
        return context
    
    
class ProductVariationPriceListView(ExtraContext, ListView):
    model = ProductVariationPrice
    template_name = "product/productvariationprice_list.html"
    
    def get_context_data(self, **kwargs):
        context = super(ProductVariationPriceListView, self).get_context_data(**kwargs)
        context['active'].append('__price')
        return context
    

class ProductVariationPriceLogListView(ExtraContext, ListView):
    model =  ProductVariationPriceLog
    ordering = '-create_date'
    template_name = "product/productvariationpricelog_list.html"
    
    def get_queryset(self):
        qs = super(ProductVariationPriceLogListView, self).get_queryset()
        if self.kwargs.get('pk'):
            qs = qs.filter(product__pk=self.kwargs.get('pk'))
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(ProductVariationPriceLogListView, self).get_context_data(**kwargs)
        context['active'].append('__price')
        return context
    
def get_product_price(request, pk):
    try:
        pp = ProductVariationPrice.objects.get(product=pk)
        return JsonResponse({"price": pp.price})
    except Exception:
        return JsonResponse({"price": "error"})
   
    
class SupplierCreateView(ExtraContext, CreateView):
    model = Supplier
    form_class = SupplierForm
    extra_context = {'active': ['_union_prod','__supplier']}
    success_url = reverse_lazy('product:supplier_list')
    
    
class SupplierUpdateView(ExtraContext, UpdateView):
    model = Supplier
    form_class = SupplierForm
    extra_context = {'active': ['__supplier']}
    success_url = reverse_lazy('product:supplier_list')
    
    
class SupplierListView(ExtraContext, ListView):
    model = Supplier
    extra_context = {'active': ['__supplier']}


class SupplierUserCreateView(CreateView):
    model = User
    form_class = SupplierUserForm
    template_name = "product/supplier_user_form.html"
    extra_context = {'active': ['__supplier']}
    # success_url = reverse_lazy('product:supplier_list')

    def form_valid(self, form):
        # f = super(SupplierUserCreateView, self).form_valid(form)
        instance = None
        try:
            while transaction.atomic():
                self.object = form.save()
                if not instance:
                    self.object.set_password(form.cleaned_data.get('password'))
                self.object.save()
                pk = self.kwargs.get('supplier')
                supplier = get_object_or_404(Supplier, pk=pk)
                profile = get_object_or_404(Profile, pk= self.object.id)

                profile.msisdn=form.cleaned_data.get('msisdn')
                profile.access_level=get_object_or_404(AccessLevel, pk=3)
                profile.save()

                SupplierAdmin.objects.create(
                    user=self.object,
                    supplier = supplier,
                    created_by =self.request.user
                )
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SupplierUserCreateView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('supplier')
        context['supplier'] = get_object_or_404(Supplier, name_iexact="supplier")
        return context

    def get_initial(self):
        initial = super(SupplierUserCreateView, self).get_initial()
        initial['instance'] = None
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(SupplierUserCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['instance'] = None
        return kwargs

    def get_success_url(self):
        return reverse('product:supplier_user_list', kwargs={'supplier': self.kwargs.get('supplier')})


class SupplierUserUpdateView(UpdateView):
    model = User
    form_class = SupplierUserForm
    # fields = '__all__'
    template_name = "product/supplier_user_form.html"
    extra_context = {'active': ['__supplier']}
    # success_url = reverse_lazy('product:supplier_list')

    def form_valid(self, form):
        # f = super(SupplierUserCreateView, self).form_valid(form)
        instance = None
        try:
            while transaction.atomic():
                self.object = form.save()
                if not instance:
                    self.object.set_password(form.cleaned_data.get('password'))
                self.object.save()
                pk = self.kwargs.get('supplier')
                supplier = get_object_or_404(Supplier, pk=pk)
                profile = get_object_or_404(Profile, pk= self.object.id)

                profile.msisdn=form.cleaned_data.get('msisdn')
                profile.access_level=get_object_or_404(AccessLevel, name__iexact="SUPPLIER")
                profile.save()

                SupplierAdmin.objects.filter(user=self.object).update(
                    supplier = supplier,
                    created_by =self.request.user
                )
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(SupplierUserUpdateView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('supplier')
        context['supplier'] = get_object_or_404(Supplier, pk=pk)
        return context

    # def get_initial(self):
    #     initial = super(SupplierUserUpdateView, self).get_initial()
    #     initial['instance'] = None
    #     return initial

    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs = super(SupplierUserUpdateView, self).get_form_kwargs(*args, **kwargs)
    #     kwargs['instance'] = None
    #     return kwargs

    def get_success_url(self):
        return reverse('product:supplier_user_list', kwargs={'supplier': self.kwargs.get('supplier')})



class SupplierUserListView(ExtraContext, ListView):
    model = SupplierAdmin
    extra_context = {'active': ['__supplier']}

    def get_queryset(self):
        queryset = super(SupplierUserListView, self).get_queryset()
        queryset = queryset.filter(supplier__id=self.kwargs.get('supplier'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super(SupplierUserListView, self).get_context_data(**kwargs)
        context['id'] = self.kwargs.get('supplier')
        return context


class ItemCreateView(ExtraContext, CreateView):
    model = Item
    form_class = ItemForm
    extra_context = {'active': ['__item']}
    success_url = reverse_lazy('product:item_list')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ItemCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        initial = None
        context = super(ItemCreateView, self).get_context_data(**kwargs)
        iformset = formset_factory(ItemAdditionChargesForm, formset=BaseFormSet, extra=1)
        formset = iformset(prefix='item_addition', initial=initial)
        context['formset'] = formset
        return context


class ItemUpdateView(ExtraContext, UpdateView):
    model = Item
    form_class = ItemForm
    extra_context = {'active': ['__item']}
    success_url = reverse_lazy('product:item_list')

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ItemUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['request'] = self.request
        return kwargs
    
    
class ItemListView(ExtraContext, ListView):
    model = Item
    extra_context = {'active': ['__Item']}

    def get_queryset(self):
        queryset = super(ItemListView, self).get_queryset()

        if self.request.user.profile.is_supplier():
            if not self.request.user.is_superuser:
                supplier = self.request.user.supplier_admin.supplier
                queryset = queryset.filter(supplier=supplier)
        return queryset


class ItemUploadView(View):
    template_name = "product/item_upload.html"

    def get(self, request, **kwargs):
        data = dict()
        data['form'] = ItemUploadForm
        return render(request, self.template_name, data)

    def post(self, request, **kwargs):
        ata = dict()
        form = ItemUploadForm(request.POST, request.FILES)
        if form.is_valid():
            f = request.FILES['excel_file']

            path = f.temporary_file_path()
            index = int(form.cleaned_data['sheet']) - 1
            startrow = int(form.cleaned_data['row']) - 1

            item_col = int(form.cleaned_data['item_col'])
            supplier_price_col = int(form.cleaned_data['supplier_price_col'])
            retail_price_col = int(form.cleaned_data['retail_price_col'])
            category_col = int(form.cleaned_data['category_column'])
            supplier = form.cleaned_data.get('supplier')

            book = xlrd.open_workbook(filename=path, logfile='/tmp/xls.log')
            sheet = book.sheet_by_index(index)
            rownum = 0
            data = dict()
            item_list = []

            for i in range(startrow, sheet.nrows):
                try:
                    row = sheet.row(i)
                    rownum = i + 1

                    item = smart_str(row[item_col].value).strip()
                    if not re.search('^[0-9A-Z\s\(\)\-\.\,]+$', item, re.IGNORECASE):
                        if (i + 1) == sheet.nrows: break
                        data['errors'] = '"%s" is not a valid Item (row %d)' % \
                                         (item, i + 1)
                        return render(request, self.template_name, {'active': 'system', 'form': form, 'error': data})

                    supplier_price = smart_str(row[supplier_price_col].value).strip()
                    if supplier_price:
                        try:
                            supplier_price = float(supplier_price)
                        except Exception as e:
                            ##print e
                            data['errors'] = '"%s" is not a valid supplier price (row %d)' % \
                                             (supplier_price, i + 1)
                            return render(request, self.template_name,
                                          {'active': 'system', 'form': form, 'error': data})
                        # if supplier_price:
                        #     if not re.search('^[0-9]+$', str(supplier_price), re.IGNORECASE):
                        #         data['errors'] = '"%s" is not a valid supplier price (row %d)' % \
                        #                          (supplier_price, i + 1)
                        #         return render(request, self.template_name,
                        #                       {'active': 'system', 'form': form, 'error': data})

                    retail_price = smart_str(row[retail_price_col].value).strip()
                    if retail_price:
                        try:
                            retail_price = float(retail_price)
                        except Exception as e:
                            data['errors'] = '"%s" is not a valid retail price (row %d)' % \
                                             (retail_price, i + 1)
                            return render(request, self.template_name,
                                          {'active': 'system', 'form': form, 'error': data})
                        # if retail_price:
                        #     if not re.search('^[0-9]+$', str(retail_price), re.IGNORECASE):
                        #         data['errors'] = '"%s" is not a valid retail price (row %d)' % \
                        #                          (retail_price, i + 1)
                        #         return render(request, self.template_name,
                        #                       {'active': 'system', 'form': form, 'error': data})

                    category = smart_str(row[category_col].value).strip()
                    if not re.search('^[A-Z\s\(\)\-\.]+$', category, re.IGNORECASE):
                        if (i + 1) == sheet.nrows: break
                        data['errors'] = '"%s" is not a valid Category (row %d)' % \
                                         (category, i + 1)
                        return render(request, self.template_name, {'active': 'system', 'form': form, 'error': data})
                    try:
                        cate = ItemCategory.objects.get(category_name__iexact=category)
                    except Exception as e:
                        data['errors'] = '"%s" is not a Category (row %d)' % \
                                         (e, i + 1)
                        return render(request, self.template_name, {'active': 'system', 'form': form, 'error': data})

                    q = {
                        'item': item,
                        'supplier_price': supplier_price,
                        'retail_price': retail_price,
                        'category': category,
                    }
                    item_list.append(q)
                except Exception as err:
                    log_error()
                    print(err)
                    return render(request, self.template_name,
                                  {'active': 'setting', 'form': form, 'error': "%s row %s" % (err, i + 1)})

            if item_list:
                with transaction.atomic():
                    try:
                        for c in item_list:
                            item = c.get('item')
                            supplier_price = c.get('supplier_price')
                            retail_price = c.get('retail_price')
                            category = c.get('category')

                            try:
                                cate = ItemCategory.objects.get(category_name__iexact=category)
                            except Exception:
                                cate= None

                            if not Item.objects.filter(name=item, category=cate, supplier=supplier).exists():
                                item = Item.objects.create(
                                    name = item,
                                    category = cate,
                                    supplier_price = supplier_price,
                                    price = retail_price,
                                    supplier = supplier,
                                    created_by = request.user
                                )
                    except Exception as err:
                        log_error()
                        log_debug(err)
                        print(err)
                        data['error'] = err

        data['form'] = form
        return render(request, self.template_name, data)

class SalesCommissionCreateView(ExtraContext, CreateView):
    model = SalesCommission
    form_class = SalesCommissionForm
    extra_context = {'active': ['_union_prod', '__commission']}
    success_url = reverse_lazy('product:commission_list')


class SalesCommissionUpdateView(ExtraContext, UpdateView):
    model = SalesCommission
    form_class = SalesCommissionForm
    extra_context = {'active': ['__commission']}
    success_url = reverse_lazy('product:commission_list')


class SalesCommissionListView(ExtraContext, ListView):
    model = SalesCommission
    extra_context = {'active': ['__commission']}


class ItemCategoryListView(ExtraContext, ListView):
    model = ItemCategory
    extra_context = {'active': ['__item']}


class ItemCategoryCreateView(ExtraContext, CreateView):
    model = ItemCategory
    form_class = ItemCategoryForm
    extra_context = {'active': ['__item']}
    success_url = reverse_lazy('product:item_category_list')


class ItemCategoryUpdateView(ExtraContext, UpdateView):
    model = ItemCategory
    form_class = ItemCategoryForm
    extra_context = {'active': ['__item']}
    success_url = reverse_lazy('product:item_category_list')




def get_item_price(request, pk):
    try:
        pp = Item.objects.get(pk=pk)
        return JsonResponse({"price": pp.price})
    except Exception:
        return JsonResponse({"price": "error"})


@csrf_exempt
def compute_item_price(request):
    payload = request.POST.get('payload')
    supplier_price = float(request.POST.get('supplier_price'))

    retail_price = 0
    charge = 0

    for data in json.loads(payload):

        if data['value']:
            charge_type = data['charge_type']
            value = float(data['value'])
            value_type = data['value_type']

            if value_type == "PERCENTAGE":
                v = supplier_price * float(value/100)

            if value_type == "AMOUNT":
                v = value

            if charge_type == "DISCOUNT":
                charge += - float(v)

            if charge_type == "CHARGE":
                charge += float(v)

    retail_price = supplier_price + charge
    print(retail_price)

    return JsonResponse({"retail_price": retail_price})


@csrf_exempt
def compute_famunera_token(request):
    try:
        clientId = request.POST.get("username")
        clientSecret = request.POST.get("password")

        fapi = FamuneraAPI({})
        pl = {
            "clientId": clientId,
            "clientSecret": clientSecret
        }
        gt = fapi.create_token(pl)
        return JsonResponse({"token": gt.get("token")})
    except Exception as e:
        log_error()
        return JsonResponse({"token": ""})