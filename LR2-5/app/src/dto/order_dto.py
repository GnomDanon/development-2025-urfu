import uuid
from typing import List

from pydantic import BaseModel


class OrderCreate(BaseModel):
    user_id: uuid.UUID
    address_id: uuid.UUID
    product_ids: List[uuid.UUID]
