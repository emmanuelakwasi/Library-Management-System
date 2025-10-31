from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Book:
    book_id: str
    title: str
    author: str
    year: str
    isbn: str
    status: str = field(default="available")  # "available" or "borrowed"
    borrowed_by: Optional[str] = field(default=None)  # member_id if borrowed
    borrowed_on: Optional[str] = field(default=None)  # ISO date string

    def is_available(self) -> bool:
        return self.status == "available"

    def borrow(self, member_id: str, date_str: str) -> bool:
        if self.is_available():
            self.status = "borrowed"
            self.borrowed_by = member_id
            self.borrowed_on = date_str
            return True
        return False

    def return_book(self) -> bool:
        if not self.is_available():
            self.status = "available"
            self.borrowed_by = None
            self.borrowed_on = None
            return True
        return False
