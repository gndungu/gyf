from __future__ import unicode_literals
import json
import datetime
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.forms.formsets import formset_factory, BaseFormSet
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from credit.models import LoanRequest, CreditManager
from credit.utils import create_loan_transaction
from coop.models import FinancialInstitution, OffTaker
from coop.forms import OrderItemForm, MemberOrderForm, OffTakerForm, FinancialInstitutionForm
from coop.views.member import save_transaction
from conf.utils import generate_alpanumeric, genetate_uuid4, log_error, log_debug, generate_numeric, float_to_intstring, get_deleted_objects,\
get_message_template as message_template


class FinancialInstitutionListView(ListView):
    model = FinancialInstitution


class FinancialInstitutionCreateView(CreateView):
    model = FinancialInstitution
    form_class = FinancialInstitutionForm
    success_url=reverse_lazy('coop:finance_list')


class FinancialInstitutionUpateView(UpdateView):
    model = FinancialInstitution
    form_class = FinancialInstitutionForm
    success_url = reverse_lazy('coop:finance_list')


class OffTakerListView(ListView):
    model = OffTaker


class OffTakerCreateView(CreateView):
    model = OffTaker
    form_class = OffTakerForm
    success_url = reverse_lazy('coop:offtaker_list')


class OffTakerUpateView(UpdateView):
    model = OffTaker
    form_class = OffTakerForm
    success_url = reverse_lazy('coop:offtaker_list')