from typing import Optional

from pydantic import BaseModel


class TerminalBase(BaseModel):
    id: int


class ProductTerminalAssignment(BaseModel):
    terminal_id: int
    product_id: Optional[int] = None
