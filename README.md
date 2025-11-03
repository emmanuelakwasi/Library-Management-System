#  Flask Library Management System (OOP + CSV)

**Created by:** Emmanuel A. Opoku  
**Course:** CS 120 – Python  
**Institution:** Grambling State University  

---

##  Project Background

This project was developed as part of our **CS 120 class activities** at **Grambling State University**, where we explored **Object-Oriented Programming (OOP)** concepts in Python and applied them to real-world applications using the **Flask web framework**.

The goal was to design a simple yet functional **Library Management System** to replace the **traditional pen-and-paper process** currently used at the **Grambling State University Library**.  

By leveraging Flask and Python OOP, this system demonstrates how small-scale automation can make library operations — such as borrowing, returning, and tracking books — more efficient and reliable.

---

## Features

- ➕ Add, view, and delete **Books**
- 👥 Add, view, and delete **Members**
- 🔄 **Borrow** and **Return** books
- 💾 Data persists in `data/*.csv` (simple database storage)
- 🧩 Clean OOP models: `Book`, `Member`, and `Library`

---

## 🗂️ Project Structure

library_app/
├── app.py
├── models/
│ ├── book.py
│ ├── member.py
│ └── library.py
├── data/
│ ├── books.csv
│ └── members.csv
├── templates/
│ ├── index.html
│ ├── add_book.html
│ ├── add_member.html
│ └── view_books.html
├── static/
│ └── style.css
└── README.md


## How to Run
1. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Run the app**
   ```bash
   python app.py
   ```

4. **Open in browser**
   Visit: http://127.0.0.1:5000

## Notes
- Borrowing requires a valid `member_id`. Add members first via **Add Member** page.
- Book IDs and Member IDs should be unique.
- CSV files are created automatically with headers.

