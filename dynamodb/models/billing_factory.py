from .billing_type import BillingType
from .billing import Billing


class BillingFactory:

    def create(self, info: dict) -> Billing:
        if 'BillingModeSummary' in info:
            billing = info['BillingModeSummary']

            return Billing(
                billing['LastUpdateToPayPerRequestDateTime'],
                BillingType(billing['BillingMode']))
