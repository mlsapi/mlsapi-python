from __future__ import annotations

from typing import Any, Dict, Optional

from mlsapi.async_http import AsyncHttpClient
from mlsapi.http import HttpClient


class BillingResource:
    """Synchronous billing and credit operations."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def get_overview(self) -> Dict[str, Any]:
        """Fetch subscription tier, credit allowances, and usage breakdown."""
        return self._http.get("/api/billing/overview")

    def create_checkout_session(
        self,
        plan_id: Optional[str] = None,
        topup_credits: Optional[int] = None,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a Stripe checkout session for plan upgrade or top-up credits."""
        payload: Dict[str, Any] = {}
        if plan_id:
            payload["planId"] = plan_id
        if topup_credits:
            payload["topupCredits"] = topup_credits
        if success_url:
            payload["successUrl"] = success_url
        if cancel_url:
            payload["cancelUrl"] = cancel_url
        return self._http.post("/api/billing/checkout", json=payload)

    def create_portal_session(self) -> Dict[str, Any]:
        """Generate self-service Stripe Customer Portal URL."""
        return self._http.post("/api/billing/portal")


class AsyncBillingResource:
    """Asynchronous billing and credit operations."""

    def __init__(self, http: AsyncHttpClient) -> None:
        self._http = http

    async def get_overview(self) -> Dict[str, Any]:
        """Fetch subscription tier, credit allowances, and usage breakdown."""
        return await self._http.get("/api/billing/overview")

    async def create_checkout_session(
        self,
        plan_id: Optional[str] = None,
        topup_credits: Optional[int] = None,
        success_url: Optional[str] = None,
        cancel_url: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a Stripe checkout session for plan upgrade or top-up credits."""
        payload: Dict[str, Any] = {}
        if plan_id:
            payload["planId"] = plan_id
        if topup_credits:
            payload["topupCredits"] = topup_credits
        if success_url:
            payload["successUrl"] = success_url
        if cancel_url:
            payload["cancelUrl"] = cancel_url
        return await self._http.post("/api/billing/checkout", json=payload)

    async def create_portal_session(self) -> Dict[str, Any]:
        """Generate self-service Stripe Customer Portal URL."""
        return await self._http.post("/api/billing/portal")
