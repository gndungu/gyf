# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.db.models import Sum
from django.views.generic import TemplateView
from django.db.models import Q, CharField, Max, Sum, Count, Value as V
from django.db.models.functions import Concat
from coop.models import *
from activity.models import *
from payment.models import *
from credit.models import *
from conf.models import *
from userprofile.models import Profile
from product.models import ProductVariationPrice, Supplier
from messaging.models import OutgoingMessages


class DashboardView(TemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        regions = []
        cooperatives = Cooperative.objects.all()
        farmer_group = FarmerGroup.objects.all()
        members = CooperativeMember.objects.all()
        suppliers = Supplier.objects.all()
        orders = MemberOrder.objects.all()
        loans = LoanRequest.objects.all()
        financial_institutions = FinancialInstitution.objects.all()
        offtakers = OffTaker.objects.all()
        sum_loans = loans.filter(status='APPROVED').aggregate(sum=Sum('requested_amount'))
        agents = Profile.objects.filter(access_level__name='AGENT')

        cooperative_contribution = CooperativeContribution.objects.all().order_by('-update_date')[:5]
        cooperative_shares = CooperativeShareTransaction.objects.all().order_by('-update_date')
        product_price = ProductVariationPrice.objects.all().order_by('-update_date')
        collections = Collection.objects.all().order_by('-update_date')
        payments = MemberPaymentTransaction.objects.all().order_by('-transaction_date')
        success_payments = payments.filter(status='SUCCESSFUL')
        training = TrainingSession.objects.all().order_by('-create_date')
        # supply_requests = MemberSupplyRequest.objects.all().order_by('-create_date')
        # supply_requests = supply_requests.filter(status='ACCEPTED')
        m_shares = CooperativeMemberSharesLog.objects
        messages = OutgoingMessages.objects.all()

        for r in Region.objects.all():
            region_members = members.filter(district__id__in=r.districts.all()).count()
            region_farmer_group = farmer_group.filter(district__id__in=r.districts.all()).count()
            region_agents = agents.filter(district__id__in=r.districts.all()).count()
            if r.name not in regions:
                regions.append({"region": r.name, "farmer_groups": region_farmer_group, "region_members": region_members, 'region_agents':region_agents})

        if not self.request.user.profile.is_union():
            if hasattr(self.request.user, 'cooperative_admin'):
                coop_admin = self.request.user.cooperative_admin.cooperative
                members = members.filter(cooperative = coop_admin)
                cooperative_shares = cooperative_shares.filter(cooperative = coop_admin)
                m_shares = m_shares.filter(cooperative_member__cooperative = coop_admin)
                collections = collections.filter(member__cooperative = coop_admin)
            if hasattr(self.request.user, 'partner_admin'):
                partner = self.request.user.partner_admin.partner
                members = members.filter(farmer_group__partner=partner)
                collections = collections.filter(member__farmer_group__partner=partner)
                farmer_group = farmer_group.filter(partner=partner)
                fg_districts = [dst.district.id for dst in farmer_group if dst.district]
                agents = agents.filter(district__id__in=fg_districts)

        if self.request.user.profile.district.all().count() > 0:
            members = members.filter(district__id__in=self.request.user.profile.district.all())
            collections = collections.filter(member__district__id__in=self.request.user.profile.district.all())
            orders = orders.filter(member__district__id__in=self.request.user.profile.district.all())
            cooperatives = cooperatives.filter(district__id__in=self.request.user.profile.district.all())
            farmer_group = farmer_group.filter(district__id__in=self.request.user.profile.district.all())
            agents = agents.filter(district__id__in=self.request.user.profile.district.all())
            regions = []
            for r in Region.objects.filter(districts__in=self.request.user.profile.district.all()):
                region_members = members.filter(district__id__in=r.districts.all()).count()
                region_farmer_group = farmer_group.filter(district__id__in=r.districts.all()).count()
                region_agents = agents.filter(district__id__in=r.districts.all()).count()
                dct={"region": r.name, "farmer_groups": region_farmer_group, "region_members": region_members,
                         'region_agents': region_agents}
                if dct not in regions:
                    regions.append(dct)

        district_summary = members.values('district__name').annotate(dc=Count('id'))
        collection_qty = collections.aggregate(total_amount=Sum('quantity'))
        collection_produce = collections.values('product__name').annotate(total_amount=Sum('quantity'))
        total_payment = success_payments.aggregate(total_amount=Sum('amount'))
        collection_amt = collections.aggregate(total_amount=Sum('total_price'))
        members_shares = members.aggregate(total_amount=Sum('shares'))
        eighteen = [f for f in members if f.age  if f.age <= 18]
        youth = [f for f in members if f.age if f.age > 18 and f.age <= 35]
        midlife = [f for f in members if f.age if f.age > 35]
        male = members.filter(Q(gender='male') | Q(gender='m'))
        female = members.filter(Q(gender='female') | Q(gender='f'))
        # members_animals = members.aggregate(total_amount=Sum('animal_count'))
        shares = cooperatives.aggregate(total_amount=Sum('shares'))
        m_shares = m_shares.values('cooperative_member',
                                   name=Concat('cooperative_member__surname',
                                               V(' '),
                                               'cooperative_member__first_name'
                                               ),
                                   
                                   ).annotate(total_amount=Sum('amount'), total_shares=Sum('shares'), transaction_date=Max('transaction_date')).order_by('-transaction_date')
        
        cooperative_shares = cooperative_shares.values('cooperative',
                                   'cooperative__name',
                                   ).annotate(total_amount=Sum('amount_paid'), total_shares=Sum('shares_bought'), transaction_date=Max('transaction_date')).order_by('-transaction_date')
        
        context['regions'] = regions
        context['cooperatives'] = cooperatives.count()
        context['farmer_group'] = farmer_group.count()
        context['suppliers'] = suppliers.count()
        context['orders'] = orders.count()
        context['loans'] = loans.count()
        context['agents'] = agents.count()
        context['financial_institutions'] = financial_institutions.count()
        context['offtakers'] = offtakers.count()
        context['agents'] = agents.count()
        context['sum_loans'] = sum_loans
        context['coop_summary'] = cooperatives
        context['district_summary'] = district_summary
        context['eighteen'] = len(eighteen)
        context['youth'] = len(youth)
        context['midlife'] = len(midlife)

        context['shares'] = shares['total_amount']
        context['transactions'] = Cooperative.objects.all().count()
        context['members'] = members.count()
        context['male'] = male.count()
        context['female'] = female.count()
        context['active'] = ['_dashboard', '']
        context['members_shares'] = members_shares['total_amount']
        context['m_shares'] = m_shares[:5]
        context['collections_latest'] = collections[:5]
        context['collections'] = collection_qty['total_amount'] or 0
        context['collection_amt'] = collection_amt['total_amount'] or 0
        context['total_payment'] = total_payment['total_amount']
        context['collection_produce'] = collection_produce

        context['cooperative_contribution'] = cooperative_contribution
        context['cooperative_shares'] = cooperative_shares[:5]
        context['training'] = training[:5]
        context['product_price'] = product_price
        context['sms'] = messages.filter(status='SENT').count()
        # context['supply_requests'] = supply_requests[:5]
        return context
    
    


