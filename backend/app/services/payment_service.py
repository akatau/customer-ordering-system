from decimal import Decimal


class PaymentService:
    @staticmethod
    def process_payment(amount: Decimal, payment_method: str) -> dict:
        if not payment_method:
            raise ValueError("Payment method is required")

        if payment_method.startswith("test_card_"):
            if payment_method == "test_card_success":
                return {"status": "succeeded", "transaction_id": "txn_test_success"}
            raise ValueError("Payment declined")

        # Stubbed external payment processing
        return {"status": "succeeded", "transaction_id": "txn_stubbed"}
