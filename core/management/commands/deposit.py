import stripe

from django.core.management import BaseCommand
from django.conf import settings

from server.account.models import Account
from server.business.models import Business, BusinessBillingInfo

stripe.api_key = settings.STRIPE_API_KEY

class Command(BaseCommand):
    help = "Deposit"

    def add_arguments(self, parser):
        parser.add_argument('managed_account_token', nargs='+', type=str)
        parser.add_argument('amount', nargs='+', type=float)

    def handle(self, *args, **options):
        response = None
        message = "Deposit"
        mat = options['managed_account_token']
        amount = options['amount']

        try:
            response = stripe.Charge.create(
                amount = amount,
                currency = "usd",
                source = managed_account_token
            )
        except stripe.error.StripeError as e:
            message = e.json_body['error']['message']

        self.stdout.write(message)