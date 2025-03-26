from tkinter import *
from tkinter import ttk
import sqlite3

# Connect to the database
db = sqlite3.connect("clients.db")
cur = db.cursor()


# ============ Main window ============
root = Tk()

root.state("zoomed")
root.title("إدارة العملاء")
root.iconbitmap(r"images\management.ico")
root.configure(background="#c2c2c2")

# ============ Variables ============
client_id = StringVar()
name = StringVar()
phone = StringVar()
email = StringVar()
gender = StringVar()
address = StringVar()


# ============ Functions ============
def add():
    pass


def update():
    pass


def delete():
    pass


def search():
    pass


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

id_lb = Label(control_frame, text="Id", **label_options)
id_lb.pack()
id_ent = Entry(control_frame, **entry_options, textvariable=client_id)
id_ent.pack()

name_lb = Label(control_frame, text="الأسم", **label_options)
name_lb.pack()
name_ent = Entry(control_frame, **entry_options, textvariable=name)
name_ent.pack()

phone_lb = Label(control_frame, text="رقم الهاتف المحمول", **label_options)
phone_lb.pack()
phone_ent = Entry(control_frame, **entry_options, textvariable=phone)
phone_ent.pack()

email_lb = Label(control_frame, text="البريد الإلكتروني", **label_options)
email_lb.pack()
email_ent = Entry(control_frame, **entry_options, textvariable=email)
email_ent.pack()

gender_lb = Label(control_frame, text="النوع", **label_options)
gender_lb.pack()
gender_ent = ttk.Combobox(
    control_frame,
    values=("ذكر", "أنثي"),
    font=("Dubai", 12),
    width=23,
    state="readonly",
    textvariable=gender,
)
gender_ent.pack()

address_lb = Label(control_frame, text="العنوان", **label_options)
address_lb.pack()
address_ent = Entry(control_frame, **entry_options, textvariable=address)
address_ent.pack()

# ========= Buttons =========
bt_options = {
    "font": ("Dubai", 12, "bold"),
    "cursor": "hand2",
    "width": 20,
    "relief": "raised",
    "bd": 2,
    "bg": "#35f8ae",
}

y = 480
x = 55
# --- Add
add_bt = Button(
    control_frame, text="إضافة", **bt_options, command=lambda: print(name.get())
)
add_bt.place(y=y, x=x)

# --- Update
update_bt = Button(control_frame, text="تحديث", **bt_options)
update_bt.place(y=y + 55, x=x)

# --- Delete
delete_bt = Button(control_frame, text="حذف", **bt_options)
delete_bt.place(y=y + 110, x=x)

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

search_img = PhotoImage(file=r"images\icons8-search-28.png")
# image=search_img,
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
    columns=("address", "email", "phone", "gender", "name", "id"),
    show="headings",
)
clients_table.place(x=18, y=0, height=610, width=1018)

clients_table.heading("id", text="Id")
clients_table.heading("name", text="الأسم")
clients_table.heading("gender", text="النوع")
clients_table.heading("phone", text="رقم الهاتف")
clients_table.heading("email", text="البريد الإلكتروني")
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

# Insert Data
clients_table.insert(
    "",
    "end",
    values=(
        "مصر, محافظة قنا, مركز فرشوط قرية العسيرات\n",
        "aaaaaadhmrabee9@.com",
        f"+962 0779529892",
        "ذكر",
        f"ادهم ربيع احمد محمد عثمان",
        1,
    ),
)
clients_table.insert(
    "",
    "end",
    values=(
        "مصر, محافظة قنا, مركز فرشوط قرية العسيرات\n",
        "aaaaaadhmrabee9@.com",
        f"+962 0779529892",
        "ذكر",
        f"رضا عبدالمنعم محمد",
        1,
    ),
)


# ============ Run App ============

root.mainloop()
