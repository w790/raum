import json
import hmac
import hashlib
import requests
from django.conf import settings

class NowPaymentsService:
    def __init__(self):
        self.api_key = settings.NOWPAYMENTS_API_KEY
        self.ipn_secret = settings.NOWPAYMENTS_IPN_SECRET
        self.base_url = "https://api.nowpayments.io/v1"

    def create_invoice(self, order, success_url, cancel_url, ipn_url):
        endpoint = f"{self.base_url}/invoice"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "price_amount": float(order.total_price),
            "price_currency": "usd",
            "order_id": str(order.id),
            "order_description": f"Order #{order.id} for {order.email}",
            "ipn_callback_url": ipn_url,
            "success_url": success_url,
            "cancel_url": cancel_url
        }
        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()

    def verify_ipn_signature(self, signature, payload):
        sorted_payload = json.dumps(payload, separators=(',', ':'), sort_keys=True)
        digest = hmac.new(
            str(self.ipn_secret).encode(),
            sorted_payload.encode(),
            hashlib.sha512
        )
        calculated_signature = digest.hexdigest()
        return hmac.compare_digest(calculated_signature, signature)
