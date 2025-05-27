"""Razorpay utility functions for creating orders."""
import razorpay
from django.conf import settings

class RazorpayUtils:

    def __init__(self) -> None:
        self.client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        self.client.set_app_details({"title" : "Movie Bazaar", "version" : "1.0.0"})


    def create_order(
            self, original_amount:float, receipt:str, currency='INR', notes=None):
        '''
        success_response example: {
            "id": "order_EKwxwAgItmmXdp",
            "entity": "order",
            "amount": 50000,
            "amount_paid": 0,
            "amount_due": 50000,
            "currency": "INR",
            "receipt": "receipt#1",
            "offer_id": null,
            "status": "created",
            "attempts": 0,
            "notes": [],
            "created_at": 1582628071
        }

        bad_response example: {
            "error": {
                "code": "BAD_REQUEST_ERROR",
                "description": "The amount must be atleast INR 1.00",
                "source": "business",
                "step": "payment_initiation",
                "reason": "input_validation_failed",
                "metadata": {},
                "field": "amount"
            }
        }
        '''
 
        response = self.client.order.create(dict(
            amount=original_amount*100,
            currency=currency,
            receipt=receipt,
            notes=notes
        ))

        return response.get('id')
    
razorpay_client = RazorpayUtils()