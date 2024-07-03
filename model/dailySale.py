from dataclasses import dataclass
from datetime import datetime


@dataclass
class DailySale:
    _Retailer_code: int
    _Product_number: int
    _Order_method_code: int
    _Date: datetime
    _Quantity: int
    _Unit_price: float
    _Unit_sale_price: float

    def __str__(self):
        return f"{self._Retailer_code}"
