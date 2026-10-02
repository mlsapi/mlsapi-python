from __future__ import annotations

from pymlsapi.async_http import AsyncHttpClient
from pymlsapi.http import HttpClient
from pymlsapi.resources.account.billing import AsyncBillingResource, BillingResource
from pymlsapi.resources.account.keys import AsyncKeysResource, KeysResource


class AccountResource:
    """Synchronous Account, Billing and Keys namespace."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http
        self.billing = BillingResource(http)
        self.keys = KeysResource(http)

    def get_billing_overview(self):
        return self.billing.get_overview()

    def verify_key(self):
        keys = self.keys.list()
        return keys[0] if keys else None


class AsyncAccountResource:
    """Asynchronous Account, Billing and Keys namespace."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http
        self.billing = AsyncBillingResource(http)
        self.keys = AsyncKeysResource(http)

    async def get_billing_overview(self):
        return await self.billing.get_overview()

    async def verify_key(self):
        keys = await self.keys.list()
        return keys[0] if keys else None
