from math import ceil
from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    page: int
    limit: int
    total: int
    pages: int


def build_page(
    items: list,
    total: int,
    page: int,
    limit: int,
) -> dict:
    return {
        "items": items,
        "page": page,
        "limit": limit,
        "total": total,
        "pages": ceil(total / limit) if total else 0,
    }
