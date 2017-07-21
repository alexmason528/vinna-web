import stripe

from django.core.management import BaseCommand
from django.conf import settings

from server.account.models import Account
from server.business.models import Business, BusinessBillingInfo

stripe.api_key = settings.STRIPE_API_KEY

class Command(BaseCommand):

    help = "Charge"

    def add_arguments(self, parser):
        parser.add_argument('partner_customer_token', type=str)
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        message = ''
        pct = options['partner_customer_token']
        amount = options['amount']

        response = None

        try:
            response = stripe.Charge.create(
                amount = amount,
                currency = "usd",
                customer = pct
            )
        except stripe.error.StripeError as e:
            message = e.json_body['error']['message']

        if response:
            message = "Charge %s %d completed - %s" % (pct, amount, response['id'])

        self.stdout.write(message)

