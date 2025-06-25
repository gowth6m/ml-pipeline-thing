from typing import Generic, List, TypeVar

from pydantic import Field

from src.models.core import CoreModel

T = TypeVar("T")


class PaginationResponse(CoreModel, Generic[T]):
    """Generic pagination response model"""

    items: List[T] = Field(..., description="List of items for the current page")
    total: int = Field(..., description="Total number of items across all pages")
    page: int = Field(..., description="Current page number (1-based)")
    size: int = Field(..., description="Number of items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")

    @classmethod
    def create(
        cls,
        items: List[T],
        total: int,
        page: int,
        size: int,
    ) -> "PaginationResponse[T]":
        """Create a pagination response with calculated metadata"""
        pages = (total + size - 1) // size
        has_next = page < pages
        has_prev = page > 1

        return cls(
            items=items,
            total=total,
            page=page,
            size=size,
            pages=pages,
            has_next=has_next,
            has_prev=has_prev,
        )
