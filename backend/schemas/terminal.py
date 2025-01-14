from typing import Optional, Dict, List

from pydantic import BaseModel


class TerminalBase(BaseModel):
    id: int


class TerminalProductAssignment(BaseModel):
    terminal_id: int
    product_id: Optional[int] = None


def convert_to_terminal_product_assignments(data: Dict[int, Optional[int]]) -> List[TerminalProductAssignment]:
    return [TerminalProductAssignment(terminal_id=terminal_id, product_id=product_id) for terminal_id, product_id in
            data.items()]
