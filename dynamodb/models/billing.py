from dataclasses import dataclass
from datetime import datetime

from .billing_type import BillingType


@dataclass
class Billing:
    last_update: datetime
    billing_type: BillingType

    def to_schema(self):
        return {
            'BillingMode': self.billing_type.value,
            'LastUpdateToPayPerRequestDateTime': self.last_update}
