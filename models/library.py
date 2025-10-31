import csv, os
from typing import List, Optional, Dict
from .book import Book
from .member import Member

BOOKS_HEADERS = ["book_id", "title", "author", "year", "isbn", "status", "borrowed_by", "borrowed_on"]
MEMBERS_HEADERS = ["member_id", "name", "email"]

class Library:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.books_file = os.path.join(data_dir, "books.csv")
        self.members_file = os.path.join(data_dir, "members.csv")
        self._ensure_files()

    def _ensure_files(self):
        if not os.path.exists(self.books_file):
            with open(self.books_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=BOOKS_HEADERS)
                writer.writeheader()
        if not os.path.exists(self.members_file):
            with open(self.members_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=MEMBERS_HEADERS)
                writer.writeheader()

    # ---------- BOOKS ----------
    def list_books(self) -> List[Book]:
        books = []
        with open(self.books_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                books.append(Book(**row))
        return books

    def add_book(self, book: Book) -> None:
        with open(self.books_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=BOOKS_HEADERS)
            writer.writerow({
                "book_id": book.book_id,
                "title": book.title,
                "author": book.author,
                "year": book.year,
                "isbn": book.isbn,
                "status": book.status,
                "borrowed_by": book.borrowed_by or "",
                "borrowed_on": book.borrowed_on or "",
            })

    def _write_books(self, books: List[Book]) -> None:
        with open(self.books_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=BOOKS_HEADERS)
            writer.writeheader()
            for b in books:
                writer.writerow({
                    "book_id": b.book_id,
                    "title": b.title,
                    "author": b.author,
                    "year": b.year,
                    "isbn": b.isbn,
                    "status": b.status,
                    "borrowed_by": b.borrowed_by or "",
                    "borrowed_on": b.borrowed_on or "",
                })

    def delete_book(self, book_id: str) -> bool:
        books = self.list_books()
        new_books = [b for b in books if b.book_id != book_id]
        if len(new_books) != len(books):
            self._write_books(new_books)
            return True
        return False

    def get_book(self, book_id: str) -> Optional[Book]:
        for b in self.list_books():
            if b.book_id == book_id:
                return b
        return None

    def borrow_book(self, book_id: str, member_id: str, date_str: str) -> bool:
        books = self.list_books()
        updated = False
        for b in books:
            if b.book_id == book_id and b.is_available():
                b.borrow(member_id, date_str)
                updated = True
                break
        if updated:
            self._write_books(books)
        return updated

    def return_book(self, book_id: str) -> bool:
        books = self.list_books()
        updated = False
        for b in books:
            if b.book_id == book_id and not b.is_available():
                b.return_book()
                updated = True
                break
        if updated:
            self._write_books(books)
        return updated

    # ---------- MEMBERS ----------
    def list_members(self) -> List[Member]:
        members = []
        with open(self.members_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                members.append(Member(**row))
        return members

    def add_member(self, member: Member) -> None:
        with open(self.members_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=MEMBERS_HEADERS)
            writer.writerow({
                "member_id": member.member_id,
                "name": member.name,
                "email": member.email,
            })

    def delete_member(self, member_id: str) -> bool:
        members = self.list_members()
        new_members = [m for m in members if m.member_id != member_id]
        if len(new_members) != len(members):
            with open(self.members_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=MEMBERS_HEADERS)
                writer.writeheader()
                for m in new_members:
                    writer.writerow({
                        "member_id": m.member_id,
                        "name": m.name,
                        "email": m.email,
                    })
            return True
        return False

    def get_member(self, member_id: str) -> Optional[Member]:
        for m in self.list_members():
            if m.member_id == member_id:
                return m
        return None
