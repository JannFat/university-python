import pyodbc
print("pyodbc is installed and working.")
conn=pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=DESKTOP-FPQ15DO;"
    "Database=master;"
    "Trusted_Connection=yes;"
    "Encrypt=no;"
)
cursor = conn.cursor()
print("Connected to SQL Server Successully.!")

conn.commit()
print("Table 'students' checked successfully")


import tkinter as tk
from tkinter import ttk   # for table

students = []  # simple in-memory database


def refresh_table():
    """Refreshes the table with the latest student data."""
    for row in table.get_children():
        table.delete(row)

    for s in students:
        table.insert("", "end", values=(s["name"], s["age"], s["grade"]))


def add_student():
    name = name_entry.get()
    age = age_entry.get()
    grade = grade_entry.get()

    if name == "" or age == "" or grade == "":
        status_label.config(text="❌ All fields required!")
        return

    students.append({"name": name, "age": age, "grade": grade})
    status_label.config(text=f"✔ Student '{name}' added!")

    clear_fields()
    refresh_table()


def select_student(event):
    """Loads selected row into input boxes."""
    selected = table.focus()
    if selected == "":
        return

    values = table.item(selected, "values")
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)

    name_entry.insert(0, values[0])
    age_entry.insert(0, values[1])
    grade_entry.insert(0, values[2])

    status_label.config(text="✔ Student loaded for update/delete")


def update_student():
    selected = table.focus()
    if selected == "":
        status_label.config(text="❌ Select a student to update.")
        return

    name = name_entry.get()
    age = age_entry.get()
    grade = grade_entry.get()

    # Update in list
    old_name = table.item(selected, "values")[0]

    for s in students:
        if s["name"] == old_name:
            s["name"] = name
            s["age"] = age
            s["grade"] = grade
            break

    status_label.config(text=f"✔ Student '{name}' updated!")
    refresh_table()
    clear_fields()


def delete_student():
    selected = table.focus()
    if selected == "":
        status_label.config(text="❌ Select a student to delete.")
        return

    name = table.item(selected, "values")[0]

    # Delete from list
    for s in students:
        if s["name"] == name:
            students.remove(s)
            break

    status_label.config(text=f"✔ Student '{name}' deleted!")
    refresh_table()
    clear_fields()


def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    grade_entry.delete(0, tk.END)


# --- GUI SETUP ---
root = tk.Tk()
root.title("Student Management Studio")
root.geometry("600x500")

# INPUT FIELDS
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root, width=30)
name_entry.pack()

tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root, width=30)
age_entry.pack()

tk.Label(root, text="Grade").pack()
grade_entry = tk.Entry(root, width=30)
grade_entry.pack()

# BUTTONS
tk.Button(root, text="Add Student", command=add_student).pack(pady=5)
tk.Button(root, text="Update Student", command=update_student).pack(pady=5)
tk.Button(root, text="Delete Student", command=delete_student).pack(pady=5)

# STUDENT TABLE
table = ttk.Treeview(root, columns=("Name", "Age", "Grade"), show="headings", height=8)
table.pack(pady=10)

table.heading("Name", text="Name")
table.heading("Age", text="Age")
table.heading("Grade", text="Grade")

table.column("Name", width=150)
table.column("Age", width=100)
table.column("Grade", width=120)

table.bind("<ButtonRelease-1>", select_student)  # load clicked row

# STATUS LABEL
status_label = tk.Label(root, text="", fg="blue")
status_label.pack()

root.mainloop()
