from messaging.utils import sendSMS
from account.utils import create_transaction
from conf.utils import log_debug, log_error, generate_numeric
from partner.models import Partner


def check_partner_url(str):
    partner = Partner.objects.filter(system_url__icontains=str)
    if partner.exists():
        partner = partner[0]
    return partner