# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from account.models import Transaction, Account
from django.views.generic import ListView, DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class ExtraContext(object):
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContext, self).get_context_data(**kwargs)

        context.update(self.extra_context)
        return context


class TransactionListview(ExtraContext, ListView):
    model = Transaction
    extra_context = {'active': ['_credit', '__transaction']}
    ordering = ('-id')
