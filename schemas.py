from pydantic import BaseModel, Field
from datetime import date, time

# Define the input receipt data.
class Item(BaseModel):
    shortDescription: str = Field(..., pattern="^[\\w\\s\\-]+$")
    price: str = Field(..., pattern="^\\d+\\.\\d{2}$")

class Receipt(BaseModel):
    retailer: str = Field(..., pattern="^[\\w\\s\\-&]+$")
    purchaseDate: date
    purchaseTime: time = Field(..., description="Format: HH:MM")
    items: list[Item] = Field(..., min_length=1)
    total: str = Field(..., pattern="^\\d+\\.\\d{2}$")