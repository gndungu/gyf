# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-08-19 22:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coop', '0001_initial'),
        ('account', '0001_initial'),
        ('product', '0001_initial'),
        ('conf', '0001_initial'),
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agent',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('userprofile.profile',),
        ),
        migrations.AddField(
            model_name='othercooperativeadmin',
            name='cooperative',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative'),
        ),
        migrations.AddField(
            model_name='othercooperativeadmin',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='othercooperativeadmin',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='other_cooperative_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='accept_processing_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_processor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_approver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='confirmed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item_user_confirm', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='created_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Item'),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='coop.MemberOrder'),
        ),
        migrations.AddField(
            model_name='membertransaction',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember'),
        ),
        migrations.AddField(
            model_name='membersupplyrequest',
            name='confirmation_logged_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='confirmer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='membersupplyrequest',
            name='cooperative_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember'),
        ),
        migrations.AddField(
            model_name='membersupplyrequest',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='accept_processing_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='processor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='confirmed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_confirm', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='cooperative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative'),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='created_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='memberorder',
            name='member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember'),
        ),
        migrations.AddField(
            model_name='farmergroupadmin',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='farmergroupadmin',
            name='farmer_group',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='coop.FarmerGroup'),
        ),
        migrations.AddField(
            model_name='farmergroupadmin',
            name='user',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='farmer_group_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='farmergroup',
            name='cooperative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coop.Cooperative'),
        ),
        migrations.AddField(
            model_name='farmergroup',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='farmergroup',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.District'),
        ),
        migrations.AddField(
            model_name='farmergroup',
            name='product',
            field=models.ManyToManyField(blank=True, to='product.Product'),
        ),
        migrations.AddField(
            model_name='farmergroup',
            name='sub_county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.SubCounty'),
        ),
        migrations.AddField(
            model_name='cooperativesharetransaction',
            name='cooperative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative'),
        ),
        migrations.AddField(
            model_name='cooperativesharetransaction',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cooperativesharetransaction',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conf.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='cooperativeshareprice',
            name='cooperative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative'),
        ),
        migrations.AddField(
            model_name='cooperativeshareprice',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cooperativemembersupply',
            name='cooperative_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember'),
        ),
        migrations.AddField(
            model_name='cooperativemembersubscriptionlog',
            name='cooperative_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember'),
        ),
        migrations.AddField(
            model_name='cooperativemembersubscriptionlog',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cooperativemembersubscriptionlog',
            name='received_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='coop.CooperativeMember'),
        ),
        migrations.AddField(
            model_name='cooperativemembershareslog',
            name='cooperative_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember'),
        ),
        migrations.AddField(
            model_name='cooperativemembershareslog',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cooperativemembershareslog',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='cooperativememberproductdefinition',
            name='cooperative_member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember'),
        ),
        migrations.AddField(
            model_name='cooperativememberproductdefinition',
            name='product_variation',
            field=models.ManyToManyField(blank=True, to='product.ProductVariation'),
        ),
        migrations.AddField(
            model_name='cooperativemember',
            name='account',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='member_account', to='account.Account'),
        ),
        migrations.AddField(
            model_name='cooperativemember',
            name='cooperative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coop.Cooperative'),
        ),
        migrations.AddField(
            model_name='cooperativemember',
            name='county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.County'),
        ),
        migrations.AddField(
            model_name='cooperativemember',
            name='create_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cooperativemember',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.District'),
        ),
        migrations.AddField(
            model_name='cooperativemember',
            name='farmer_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coop.FarmerGroup'),
        ),
        migrations.AddField(
            model_name='cooperativemember',
            name='parish',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.Parish'),
        ),
        migrations.AddField(
            model_name='cooperativemember',
            name='sub_county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.SubCounty'),
        ),
        migrations.AddField(
            model_name='cooperativecontribution',
            name='cooperative',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative'),
        ),
        migrations.AddField(
            model_name='cooperativecontribution',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cooperativecontribution',
            name='payment_method',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conf.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='cooperativeadmin',
            name='cooperative',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative'),
        ),
        migrations.AddField(
            model_name='cooperativeadmin',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cooperativeadmin',
            name='user',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='cooperative_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cooperative',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cooperative',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.District'),
        ),
        migrations.AddField(
            model_name='cooperative',
            name='product',
            field=models.ManyToManyField(blank=True, to='product.Product'),
        ),
        migrations.AddField(
            model_name='cooperative',
            name='sub_county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.SubCounty'),
        ),
        migrations.AddField(
            model_name='collection',
            name='cooperative',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.Cooperative'),
        ),
        migrations.AddField(
            model_name='collection',
            name='created_by',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collection',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='coop.CooperativeMember'),
        ),
        migrations.AddField(
            model_name='collection',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.ProductVariation'),
        ),
        migrations.AlterUniqueTogether(
            name='cooperativeshareprice',
            unique_together=set([('price', 'current')]),
        ),
        migrations.AlterUniqueTogether(
            name='cooperativemembersubscriptionlog',
            unique_together=set([('cooperative_member', 'year')]),
        ),
    ]