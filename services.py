from schemas import Receipt
import uuid

class Services:
    receipts = {}

    def _calculate_points(receipt: Receipt) -> int:
        points = 0
        # One point for every alphanumeric character in the retailer name.
        points += len([c for c in receipt.retailer if c.isalnum()])
        # 50 points if the total is a round dollar amount with no cents.
        if receipt.total.endswith(".00"):
            points += 50
        # 25 points if the total is a multiple of 0.25.
        if float(receipt.total) % 0.25 == 0:
            points += 25
        # 5 points for every two items on the receipt.
        points += len(receipt.items) // 2 * 5
        # If the trimmed length of the item description is a multiple of 3,
        # multiply the price by 0.2 and round up to the nearest integer.
        for item in receipt.items:
            if len(item.shortDescription.strip()) % 3 == 0:
                points += int(float(item.price) * 0.2 + 0.999)
        # 6 points if the day in the purchase date is odd.
        if receipt.purchaseDate.day % 2 == 1:
            points += 6
        # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
        if receipt.purchaseTime.hour >= 14 and receipt.purchaseTime.hour < 16:
            points += 10
        return points

    @classmethod
    def calculate_points_and_generate_id(cls, receipt: Receipt) -> str:
        id = str(uuid.uuid4())
        cls.receipts[id] = cls._calculate_points(receipt)
        return id
    
    @classmethod
    def retrieve_points(cls, id: str) -> int:
        return cls.receipts[id] if id in cls.receipts else None