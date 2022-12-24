# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import transaction
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from conf.utils import log_debug, log_error
from partner.models import *
from userprofile.models import AccessLevel
from partner.forms import PartnerForm, PartnerStaffForm, PartnerStaffChangeForm

class ExtraContext(object):
    extra_context = {}
    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)
        context['active'] = ['_partner']
        context['title'] = 'Country'
        context.update(self.extra_context)
        return context


class PartnerListView(ExtraContext, ListView):
    model = Partner


class PartnerCreateView(ExtraContext, CreateView):
    model = Partner
    form_class = PartnerForm
    template_name = "partner/partnercreate_form.html"
    success_url = reverse_lazy('partner:list')


class PartnerUpdateView(ExtraContext, UpdateView):
    model = Partner
    form_class = PartnerForm
    template_name = "partner/partnercreate_form.html"
    success_url = reverse_lazy('partner:list')
    

class PartnerDetailView(ExtraContext, DetailView):
    model = Partner
    template_name = "partner/partner_detail.html"


class PartnerStaffListView(ExtraContext, ListView):
    model = PartnerStaff
    
    def get_queryset(self):
        partner = self.kwargs.get('pk')
        if self.request.user.profile.is_partner():
            if hasattr(self.request.user, 'partner_admin'):
                partner = self.request.user.partner_admin.partner.id
        qs = super(PartnerStaffListView, self).get_queryset()
        print(partner)
        qs = qs.filter(partner__id=partner)
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(PartnerStaffListView, self). get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        if hasattr(self.request.user, 'partner_admin'):
            partner = self.request.user.partner_admin.partner
            pk = partner.id
        context['partner'] = Partner.objects.get(pk=pk)
        return context


class PartnerStaffCreateView(ExtraContext, CreateView):
    model = User
    form_class = PartnerStaffForm
    template_name = "partner/partnerstaffcreate_form.html"
    #success_url = reverse_lazy('partner:list')
    
    def form_invalid(self, form):
        return super(PartnerStaffCreateView, self).form_invalid(form)

    def form_valid(self, form):
        try:
            with transaction.atomic():
                pform = super(PartnerStaffCreateView, self).form_valid(form)
                partner = get_object_or_404(Partner, pk=self.kwargs.get('pk'))
                user = self.object
                try:
                    PartnerStaff.objects.create(user=user, partner=partner)
                except Exception as e:
                    err = "Partner access level not found"
                    form.add_error('', e)
                    return super(PartnerStaffCreateView, self).form_invalid(form)
                user.profile.access_level = AccessLevel.objects.get(name='PARTNER')
                user.profile.msisdn = form.cleaned_data.get('phone_number')
                user.profile.district = form.cleaned_data.get('district')
                user.profile.save()
                return pform

        except Exception as e:
            log_error()
            form.add_error('', e)
            return super(PartnerStaffCreateView, self).form_invalid(form)


    def form_valid_deprecated(self, form):
        try:
            with transaction.atomic():
                form.instance.created_by = self.request.user
                username =  form.cleaned_data.get('username')
                password =  form.cleaned_data.get('password')

                if PartnerStaff.objects.filter(phone_number=form.instance.phone_number).exists():
                    form.add_error('phone_number', 'The Phone Number %s exists. Please provide another.' % form.instance.phone_number)
                    return super(PartnerStaffCreateView, self).form_invalid(form)

                try:
                    user, created = User.objects.get_or_create(username=username, email=form.instance.email)
                except Exception as e:
                    log_error()
                    form.add_error('username', e)
                    return super(PartnerStaffUpdateView, self).form_invalid(form)
                if created:
                    user.set_password(password)
                    user.save()
                try:
                    user.profile.access_level=AccessLevel.objects.get(name='PARTNER')
                    user.profile.msisdn = form.cleaned_data.get('msisdn')
                    user.is_active = form.cleaned_data.get('is_active')
                except Exception as e:
                    err = "Partner access level not found"
                    form.add_error('', e)
                    return super(PartnerStaffCreateView, self).form_invalid(form)
                user.save()
                form.instance.user = user
                return super(PartnerStaffCreateView, self).form_valid(form)
        except Exception as e:
            log_error()
            form.add_error('', e)
            return super(PartnerStaffCreateView, self).form_invalid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('partner:staff_list', args = self.kwargs.get('pk'))
    
    def get_context_data(self, **kwargs):
        context = super(PartnerStaffCreateView, self). get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        
        context['partner'] = Partner.objects.get(pk=pk)
        return context
    
 
class PartnerStaffUpdateView(ExtraContext, UpdateView):
    model = User
    form_class = PartnerStaffChangeForm
    template_name = "partner/partnerstaffcreate_form.html"

    def form_valid(self, form):
        try:
            with transaction.atomic():
                pform = super(PartnerStaffUpdateView, self).form_valid(form)
                partner = get_object_or_404(Partner, pk=self.kwargs.get('code'))
                user = self.object
                try:
                    PartnerStaff.objects.filter(user=user).update(partner=partner)
                except Exception as e:
                    err = "Partner access level not found"
                    form.add_error('', e)
                    return super(PartnerStaffUpdateView, self).form_invalid(form)
                user.profile.access_level = AccessLevel.objects.get(name='PARTNER')
                user.profile.msisdn = form.cleaned_data.get('phone_number')
                user.profile.district = form.cleaned_data.get('district')
                user.profile.save()
                return pform

        except Exception as e:
            log_error()
            form.add_error('', e)
            return super(PartnerStaffUpdateView, self).form_invalid(form)

    def form_valid_dep(self, form):
        form.instance.created_by = self.request.user
        username = form.cleaned_data.get('username')
        try:
            user, created = User.objects.get_or_create(username=username, email='')
            user.profile.access_level=AccessLevel.objects.get(name='PARTNER')
            user.profile.msisdn=form.cleaned_data.get('msisdn')
            user.is_active=form.cleaned_data.get('is_active')
            user.email=form.cleaned_data.get('email')
            user.save()
            form.instance.user = user
        except Exception as e:
            log_error()
            form.add_error('', e)
            return super(PartnerStaffUpdateView, self).form_invalid(form)

        try:
            return super(PartnerStaffUpdateView, self).form_valid(form)
        except  Exception as e:
            log_error()
            form.add_error('', e)
            return super(PartnerStaffUpdateView, self).form_invalid(form)
    
    def get_success_url(self, **kwargs):         
        return reverse_lazy('partner:staff_list', args = self.kwargs.get('code'))
    
    def get_context_data(self, **kwargs):
        context = super(PartnerStaffUpdateView, self). get_context_data(**kwargs)
        pk = self.kwargs.get('code')

        context['partner'] = Partner.objects.get(pk=pk)
        return context
    
    def get_initial (self):
        initial = super(PartnerStaffUpdateView, self).get_initial()
        pk = self.kwargs.get('pk')
        user = get_object_or_404(User, pk=pk)
        initial['district'] = user.profile.district.all()
        initial['phone_number'] = user.profile.msisdn
        print(user.profile.district.all())
        return initial

