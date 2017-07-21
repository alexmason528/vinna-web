import stripe

from django.core.management import BaseCommand
from django.conf import settings

from server.account.models import Account
from server.business.models import Business, BusinessBillingInfo

stripe.api_key = settings.STRIPE_API_KEY

class Command(BaseCommand):

    help = "Deposit"

    def add_arguments(self, parser):
        parser.add_argument('managed_account_token', type=str)
        parser.add_argument('amount', type=int)

    def handle(self, *args, **options):
        message = ''
        mat = options['managed_account_token']
        amount = options['amount']

        response = None

        try:
            response = stripe.Transfer.create(
                amount=amount,
                currency="usd",
                destination=mat
            )
        except stripe.error.StripeError as e:
            message = e.json_body['error']['message']

        if response:
            message = "Deposit %s %d completed - %s" % (mat, amount, response['id'])

        self.stdout.write(message)
