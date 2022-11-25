from pydantic import BaseModel, Field
from typing import Union

class Person(BaseModel):
    name: str
    last_name: str

class Item(BaseModel):
    serial_number : Union[str,None] = Field(
        default=None, title="8 characters serial code", max_length=8)
    description : Union[str,None] = Field(
        default=None, title="The description of the item", max_length=256)
    stock_number : Union[int, None] = Field(
        default=0, title="Item stock number on inventory")

