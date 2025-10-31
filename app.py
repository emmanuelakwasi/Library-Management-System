from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import date
from models.library import Library
from models.book import Book
from models.member import Member

app = Flask(__name__)
app.secret_key = "dev-secret"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

library = Library(DATA_DIR)

@app.route("/")
def index():
    return render_template("index.html")

# -------- BOOKS --------
@app.route("/books")
def view_books():
    books = library.list_books()
    members = library.list_members()
    return render_template("view_books.html", books=books, members=members)

@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book_id = request.form.get("book_id").strip()
        title = request.form.get("title").strip()
        author = request.form.get("author").strip()
        year = request.form.get("year").strip()
        isbn = request.form.get("isbn").strip()

        if not all([book_id, title, author, year, isbn]):
            flash("All fields are required.", "error")
            return redirect(url_for("add_book"))

        # Basic uniqueness check for book_id
        if library.get_book(book_id) is not None:
            flash("Book ID already exists.", "error")
            return redirect(url_for("add_book"))

        b = Book(book_id=book_id, title=title, author=author, year=year, isbn=isbn)
        library.add_book(b)
        flash("Book added successfully.", "success")
        return redirect(url_for("view_books"))
    return render_template("add_book.html")

@app.route("/books/delete/<book_id>", methods=["POST"])
def delete_book(book_id):
    ok = library.delete_book(book_id)
    flash("Book deleted." if ok else "Book not found.", "info")
    return redirect(url_for("view_books"))

@app.route("/books/borrow", methods=["POST"])
def borrow_book():
    book_id = request.form.get("book_id")
    member_id = request.form.get("member_id")
    if not book_id or not member_id:
        flash("Please select a book and a member.", "error")
        return redirect(url_for("view_books"))
    today = date.today().isoformat()
    ok = library.borrow_book(book_id, member_id, today)
    flash("Borrowed successfully." if ok else "Book not available.", "info")
    return redirect(url_for("view_books"))

@app.route("/books/return/<book_id>", methods=["POST"])
def return_book(book_id):
    ok = library.return_book(book_id)
    flash("Returned successfully." if ok else "Book not found or already available.", "info")
    return redirect(url_for("view_books"))

# -------- MEMBERS --------
@app.route("/members")
def view_members():
    members = library.list_members()
    return render_template("view_members.html", members=members)

@app.route("/members/add", methods=["GET", "POST"])
def add_member():
    if request.method == "POST":
        member_id = request.form.get("member_id").strip()
        name = request.form.get("name").strip()
        email = request.form.get("email").strip()
        if not all([member_id, name, email]):
            flash("All fields are required.", "error")
            return redirect(url_for("add_member"))

        if library.get_member(member_id) is not None:
            flash("Member ID already exists.", "error")
            return redirect(url_for("add_member"))

        m = Member(member_id=member_id, name=name, email=email)
        library.add_member(m)
        flash("Member added successfully.", "success")
        return redirect(url_for("view_members"))
    return render_template("add_member.html")

@app.route("/members/delete/<member_id>", methods=["POST"])
def delete_member(member_id):
    ok = library.delete_member(member_id)
    flash("Member deleted." if ok else "Member not found.", "info")
    return redirect(url_for("view_members"))

if __name__ == "__main__":
    app.run(debug=True)
