from typing import List, Dict, Optional

from fastapi import APIRouter

from raspberry_interactions import ServerCommunications
from schemas.terminal import TerminalProductAssignment, convert_to_terminal_product_assignments

router = APIRouter()


@router.get("/", response_model=List[int])
def read_terminals():
    return ServerCommunications().registered_terminals


@router.get("/products/", response_model=List[TerminalProductAssignment])
def read_terminals_products_assignments():
    return convert_to_terminal_product_assignments(ServerCommunications().terminals_products_dict)


@router.put("/products/", response_model=List[TerminalProductAssignment])
def update_terminals_products_assignments(terminal_id: int, product_id: Optional[int] = None):
    ServerCommunications().terminals_products_dict[terminal_id] = product_id
    return convert_to_terminal_product_assignments(ServerCommunications().terminals_products_dict)
