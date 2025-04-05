from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# ============ Database ============

# Connect to the database
with sqlite3.connect("clients.db") as conn:
    cur = conn.cursor()

    # Create Table
    cur.execute(
        """CREATE TABLE IF NOT EXISTS clients (
      address TEXT,
      gender TEXT,
      email TEXT UNIQUE,
      phone TEXT,
      name TEXT,
      id INTEGER PRIMARY KEY
      )"""
    )
    conn.commit()


# ============ Main window ============
root = Tk()

root.state("zoomed")
root.title("إدارة العملاء")
root.iconbitmap(r"images\management.ico")
root.configure(background="#c2c2c2")

# ============ Variables ============
name = StringVar()
gender = StringVar()
phone = StringVar()
email = StringVar()
address = StringVar()
client_id = StringVar()


# ============ Functions ============
def felids_not_empty():
    felids = [name.get(), gender.get(), phone.get(), email.get(), address.get()]
    for i in felids:
        if len(i) < 2:
            return False
    else:
        return True


def shows_clients():
  
    cur.execute("SELECT * FROM `clients`")
    rows = cur.fetchall()
    clients_table.delete(*clients_table.get_children())
    for row in rows:
        clients_table.insert("", "end", values=row)
        conn.commit()


def add_client():
    if felids_not_empty():
        try:
            with sqlite3.connect("clients.db") as conn:
                cur = conn.cursor()

                cur.execute(
                    f"""INSERT INTO `clients` (address,gender,email,phone,name) VALUES(
                ?,?,?,?,?)""",
                    (
                        address.get(),
                        gender.get(),
                        email.get(),
                        phone.get(),
                        name.get(),
                    ),
                )
                conn.commit()
        except:
            messagebox.showerror(title="Error", message="البريد الإلكتروني موجود")

    else:
        messagebox.showerror(title="Error", message="لا يمكن إضافة حقل فارغ")

    shows_clients()


def delete_client():
    cursor_row = clients_table.focus()
    client_id_to_del = clients_table.item(cursor_row)["values"][5]
    print(client_id_to_del)

    if messagebox.askquestion(title="حذف عميل", message="حذف العميل") == "yes":
        with sqlite3.connect("clients.db") as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM `clients` WHERE id = ?", (client_id_to_del,))
            conn.commit()
        shows_clients()


def update():
    pass


def search():
    pass


def empty_felids():
    name.set("")
    phone.set("")
    email.set("")
    gender.set("")
    address.set("")


# ============ Control Panel ============
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Dubai", 12))
control_panel = ttk.Notebook(root)
control_panel.place(x=1050, y=1)

control_frame = Frame(root, bg="#f2f3f4", bd=2, relief="sunken", width=300, height=700)
control_frame.pack()

details_frame = Frame(root, bg="#f2f3f4", bd=2, relief="sunken", width=300, height=700)
details_frame.pack()

control_panel.add(details_frame, text="التفاصيل")
control_panel.add(control_frame, text="الإدارة")
control_panel.select(control_frame)

# Elements Options
label_options = {"bg": "#f2f3f4", "font": ("Dubai", 13, "bold")}
entry_options = {
    "bg": "white",
    "font": ("Dubai", 13),
    "bd": 2,
    "justify": "center",
    "width": 25,
    "relief": "ridge",
}

frame_title_options = {
    "font": ("Dubai", 13, "bold"),
    "bg": "#1ce1c9",
    "relief": "groove",
}

# ----------- Control Elements -----------
# -- Addition
add_title = Label(control_frame, text="إضافة عميل", **frame_title_options)
add_title.pack(fill=X)

name_lb = Label(control_frame, text="الأسم", **label_options)
name_lb.pack()
name_ent = Entry(control_frame, **entry_options, textvariable=name)
name_ent.pack()

gender_lb = Label(control_frame, text="النوع", **label_options)
gender_lb.pack()
gender_ent = ttk.Combobox(
    control_frame,
    values=("ذكر", "أنثي"),
    font=("Dubai", 12),
    width=23,
    state="readonly",
    textvariable=gender,
    justify="center",
)
gender_ent.pack()

phone_lb = Label(control_frame, text="رقم الهاتف المحمول", **label_options)
phone_lb.pack()
phone_ent = Entry(control_frame, **entry_options, textvariable=phone)
phone_ent.pack()

email_lb = Label(control_frame, text="البريد الإلكتروني", **label_options)
email_lb.pack()
email_ent = Entry(control_frame, **entry_options, textvariable=email)
email_ent.pack()


address_lb = Label(control_frame, text="العنوان", **label_options)
address_lb.pack()
address_ent = Entry(control_frame, **entry_options, textvariable=address)
address_ent.pack()


# ========= Buttons =========
bt_options = {
    "font": ("Dubai", 11, "bold"),
    "cursor": "hand2",
    "width": 20,
    "relief": "raised",
    "bd": 2,
    "bg": "#35f8ae",
}

# place value
y = 400
x = 60

# --- Add
add_bt = Button(control_frame, text="إضافة", **bt_options, command=add_client)

add_bt.place(y=y, x=x)

# --- Update
update_bt = Button(control_frame, text="تحديث", **bt_options)
update_bt.place(y=y + 55, x=x)

# --- Delete
delete_bt = Button(
    control_frame,
    text="حذف",
    **bt_options,
    command=delete_client,
)
delete_bt.place(y=y + 110, x=x)

# --- Clear
clear_bt = Button(
    control_frame,
    text="إفراغ الحقول",
    **bt_options,
    command=empty_felids,
)
clear_bt.place(y=y + 165, x=x)


# ============  Search ============
search_frame = Frame(root, bg="#f2f3f4", bd=2, relief="sunken", width=1040, height=60)
search_frame.place(y=2, x=5)
x = 600
search_ent = Entry(
    search_frame,
    font=("Dubai", 11),
    relief="ridge",
    justify="center",
    bd=2,
    width=50,
)
search_ent.place(x=x, y=10)

search_bt = Button(
    search_frame,
    text="بحث",
    font=("", 11, "bold"),
    width=8,
    bg="#35f8ae",
    cursor="hand2",
    relief="raised",
)
search_bt.place(x=x - 85, y=10)

# ============ Menubar ============
menubar = Menu(root)
options = Menu(menubar, tearoff=False)
options.add_command(label="إعادة تعيين")

menubar.add_cascade(label="خيارات", menu=options)
root.config(menu=menubar)

# ============ Show clients ============

clients_frame = Frame(root, bg="white", width=1040, height=630, bd=2, relief="sunken")
clients_frame.place(x=5, y=70)

# Configure Treeview
style.configure("Treeview.Heading", font=("Dubai", 13, "bold"))
style.configure("Treeview", font=("Dubai", 11, ""))
style.configure("Treeview", rowheight=35)

# Create Treeview
clients_table = ttk.Treeview(
    clients_frame,
    columns=("address", "gender", "email", "phone", "name", "id"),
    show="headings",
)
clients_table.place(x=18, y=0, height=610, width=1018)

clients_table.heading("id", text="Id")
clients_table.heading("name", text="الأسم")
clients_table.heading("phone", text="رقم الهاتف")
clients_table.heading("email", text="البريد الإلكتروني")
clients_table.heading("gender", text="النوع")
clients_table.heading("address", text="العنوان")

# Format Columns
clients_table.column("id", anchor="center", width=30)
clients_table.column("name", anchor="center", width=180)
clients_table.column("gender", anchor="center", width=60)
clients_table.column("phone", anchor="center", width=150)
clients_table.column("email", anchor="center", width=180)
clients_table.column("address", anchor="center", width=239)

# Scrollbar
scroll_x = Scrollbar(clients_frame, orient=HORIZONTAL, command=clients_table.xview)
scroll_x.place(x=1, y=610, width=1035)

scroll_y = Scrollbar(clients_frame, orient=VERTICAL, command=clients_table.yview)
scroll_y.place(x=1, height=610)

clients_table.config(xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)


shows_clients()


# ============ Run App ============
root.mainloop()
