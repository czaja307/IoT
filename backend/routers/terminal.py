from typing import List, Dict, Optional

from fastapi import APIRouter

from raspberry_interactions import ServerCommunications

router = APIRouter()


@router.get("/", response_model=List[int])
def read_terminals():
    return ServerCommunications().registered_terminals


@router.get("/products/", response_model=Dict[int, Optional[int]])
def read_terminals_products_assignments():
    return ServerCommunications().terminals_products_dict
