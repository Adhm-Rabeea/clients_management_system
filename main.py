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
class ManagementSystem:
    def __init__(self, root):

        self.root = root
        self.root.state("zoomed")
        # root.resizable(True,False)
        self.root.title("إدارة العملاء")
        self.root.iconbitmap(r"images\management.ico")
        self.root.configure(background="#c2c2c2")

        # ============ Variables ============
        self.name = StringVar()
        self.gender = StringVar()
        self.phone = StringVar()
        self.email = StringVar()
        self.address = StringVar()
        self.client_id = StringVar()
        self.search_var = StringVar()

        # ============ Control Panel ============
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Dubai", 12))
        control_panel = ttk.Notebook(root)
        control_panel.place(x=1050, y=1)

        control_frame = Frame(
            root, bg="#f2f3f4", bd=2, relief="sunken", width=300, height=640
        )
        control_frame.pack()

        details_frame = Frame(
            root, bg="#f2f3f4", bd=2, relief="sunken", width=300, height=640
        )
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
        name_ent = Entry(control_frame, **entry_options, textvariable=self.name)
        name_ent.pack()

        gender_lb = Label(control_frame, text="النوع", **label_options)
        gender_lb.pack()
        gender_ent = ttk.Combobox(
            control_frame,
            values=("ذكر", "أنثي"),
            font=("Dubai", 12),
            width=23,
            state="readonly",
            textvariable=self.gender,
            justify="center",
        )
        gender_ent.pack()

        phone_lb = Label(control_frame, text="رقم الهاتف المحمول", **label_options)
        phone_lb.pack()
        phone_ent = Entry(control_frame, **entry_options, textvariable=self.phone)
        phone_ent.pack()

        email_lb = Label(control_frame, text="البريد الإلكتروني", **label_options)
        email_lb.pack()
        email_ent = Entry(control_frame, **entry_options, textvariable=self.email)
        email_ent.pack()

        address_lb = Label(control_frame, text="العنوان", **label_options)
        address_lb.pack()
        address_ent = Entry(control_frame, **entry_options, textvariable=self.address)
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
        add_bt = Button(
            control_frame, text="إضافة", **bt_options, command=self.add_client
        )

        add_bt.place(y=y, x=x)

        # --- Update
        update_bt = Button(
            control_frame, text="تحديث", **bt_options, command=self.update_client
        )
        update_bt.place(y=y + 55, x=x)

        # --- Clear
        clear_bt = Button(
            control_frame,
            text="إفراغ الحقول",
            **bt_options,
            command=self.empty_felids,
        )
        clear_bt.place(y=y + 110, x=x)

        # ============  Search ============
        self.search_frame = Frame(
            root, bg="#f2f3f4", bd=2,  width=1044, height=45
        )
        self.search_frame.place(y=2, x=5)

        x = 350
        search_ent = Entry(
            self.search_frame,
            font=("Dubai", 11),
            relief="ridge",
            justify="center",
            bd=2,
            width=50,
            textvariable=self.search_var,
        )
        search_ent.place(x=x, y=2)

        search_bt = Button(
            self.search_frame,
            text="بحث",
            font=("", 10, "bold"),
            width=8,
            bg="#35f8ae",
            cursor="hand2",
            relief="raised",
            command=self.search,
        )
        search_bt.place(x=x - 80, y=4)

        # ============ Menubar ============
        menubar = Menu(root)
        options = Menu(menubar, tearoff=False)
        options.add_command(label="إعادة تعيين")

        menubar.add_cascade(label="خيارات", menu=options)
        root.config(menu=menubar)

        # --- Menu click
        self.right_click_menu = Menu(root, tearoff=0)
        self.right_click_menu.add_command(label="تعديل", command=self.fetch_client_data)
        self.right_click_menu.add_command(label="حذف", command=self.delete_client)

        # ============ Show clients ============
        self.clients_frame = Frame(
            root, bg="white", width=1044, height=634, bd=2, relief="sunken"
        )
        self.clients_frame.place(x=5, y=45)

        self.info_frame = Frame(self.clients_frame, bd=2, bg="#c2c2c2")
        self.info_frame.place(x=1, y=608, height=23, width=1040)

        # Configure Treeview
        style.configure("Treeview.Heading", font=("Dubai", 13, "bold"))
        style.configure("Treeview", font=("Dubai", 11, ""))
        style.configure("Treeview", rowheight=35)

        # Create Treeview
        self.clients_table = ttk.Treeview(
            self.clients_frame,
            columns=("address", "gender", "email", "phone", "name", "id"),
            show="headings",
        )
        self.clients_table.place(x=18, y=0, height=590, width=1040)

        self.clients_table.heading("id", text="Id")
        self.clients_table.heading("name", text="الأسم")
        self.clients_table.heading("phone", text="رقم الهاتف")
        self.clients_table.heading("email", text="البريد الإلكتروني")
        self.clients_table.heading("gender", text="النوع")
        self.clients_table.heading("address", text="العنوان")

        # Format Columns
        self.clients_table.column("id", anchor="center", width=30)
        self.clients_table.column("name", anchor="center", width=180)
        self.clients_table.column("gender", anchor="center", width=60)
        self.clients_table.column("phone", anchor="center", width=150)
        self.clients_table.column("email", anchor="center", width=180)
        self.clients_table.column("address", anchor="center", width=239)
        self.clients_table.bind("<Button-3>", self.right_click)
        self.clients_table.bind("<Double-1>", self.client_widow)

        # Scrollbar
        scroll_x = Scrollbar(
            self.clients_frame, orient=HORIZONTAL, command=self.clients_table.xview
        )
        scroll_x.place(x=1, y=590, width=1040)

        scroll_y = Scrollbar(
            self.clients_frame, orient=VERTICAL, command=self.clients_table.yview
        )
        scroll_y.place(x=1, height=590)

        self.clients_table.config(
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )

        self.shows_clients()

        # ============ Events ============

    def right_click(self, event):
        item = self.clients_table.identify_row(event.y)
        if item:
            self.clients_table.selection_set(item)
            self.right_click_menu.tk_popup(event.x_root, event.y_root)  # عرض القائمة

    # ============ Functions ============
    def felids_not_empty(self):
        felids = [
            self.name.get(),
            self.gender.get(),
            self.phone.get(),
            self.email.get(),
            self.address.get(),
        ]
        for i in felids:
            if len(i) < 2:
                return False
        else:
            return True

    def shows_clients(self):

        with sqlite3.connect("clients.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM `clients`")
            rows = cur.fetchall()

            # Show clients count in search frame
            clients_count = len(rows)
            count_lb = Label(
                self.info_frame,
                text=f"Count: {clients_count}",
                font=("", 10, ""),
                bg="#c2c2c2",
            )
            count_lb.place(x=10)

            # count_value = Label(
            #     self.info_frame,
            #     text=clients_count,
            #     font=("", 10, "bold"),
            #     bg="#c2c2c2",
            #     width=4
            # )
            # count_value.place(x=55)

        # Show clients in treeview
        self.clients_table.delete(*self.clients_table.get_children())
        for row in rows:
            self.clients_table.insert("", "end", values=row)
            conn.commit()

    def add_client(self):
        if self.felids_not_empty():
            try:
                with sqlite3.connect("clients.db") as conn:
                    cur = conn.cursor()

                    cur.execute(
                        f"""INSERT INTO `clients` (address,gender,email,phone,name) VALUES(
                  ?,?,?,?,?)""",
                        (
                            self.address.get().strip(),
                            self.gender.get().strip(),
                            self.email.get().strip(),
                            self.phone.get().strip(),
                            self.name.get().strip(),
                        ),
                    )
                    conn.commit()
                    self.empty_felids()
                messagebox.showinfo(title="إضافة", message="نم إضافة العميل بنجاح")


            except:
                messagebox.showerror(title="Error", message="البريد الإلكتروني موجود")

        else:
            messagebox.showerror(title="Error", message="لا يمكن إضافة حقل فارغ")

        self.shows_clients()

    def delete_client(self):
        cursor_row = self.clients_table.selection()
        client_id_to_del = self.clients_table.item(cursor_row)["values"][5]

        if messagebox.askquestion(title="حذف عميل", message="حذف العميل") == "yes":
            with sqlite3.connect("clients.db") as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM `clients` WHERE id = ?", (client_id_to_del,))
                conn.commit()
            self.shows_clients()

    def update_client(self):
        cursor_row = self.clients_table.selection()
        self.selected_client_id = self.clients_table.item(cursor_row)["values"]

        if self.selected_client_id:
            with sqlite3.connect("clients.db") as conn:  #
                cur = conn.cursor()
                cur.execute(
                    "UPDATE `clients` SET address = ?, email = ?, phone = ?, gender = ?, name = ? WHERE id = ?",
                    (
                        self.address.get().strip(),
                        self.email.get().strip(),
                        self.phone.get().strip(),
                        self.gender.get().strip(),
                        self.name.get().strip(),
                        self.selected_client_id[5],
                    ),
                )
                conn.commit()
            self.shows_clients()
            self.empty_felids()
            messagebox.showinfo(title="تحديث",message="تم تحديث بيانات العميل بنجاح")

    def search(self):

        with sqlite3.connect("clients.db") as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT * FROM `clients` 
                WHERE `id` = ? 
                OR 
                `name` LIKE ? 
                OR 
                `email` LIKE ? 
                OR 
                `phone` LIKE ? 
                OR 
                `address` LIKE ? 
                """,
                (
                    self.search_var.get(),
                    f"%{self.search_var.get()}%",
                    f"%{self.search_var.get()}%",
                    f"{self.search_var.get()}%",
                    f"%{self.search_var.get()}%",
                ),
            )
            rows = cur.fetchall()

            # Show clients count in search frame
            clients_count = len(rows)
            count_lb = Label(
                self.info_frame,
                text=f"Count: {clients_count}",
                font=("", 10, ""),
                bg="#c2c2c2",
                width=10,
            )
            count_lb.place(x=1)

        # Show clients in treeview
        self.clients_table.delete(*self.clients_table.get_children())
        for row in rows:
            self.clients_table.insert("", "end", values=row)
            conn.commit()

    def client_widow(self, event):
        selected = self.clients_table.selection()
        if selected:
            window = Tk()
            window.geometry("400x400")
            window.iconbitmap(r"images\management.ico")
            window.configure(background="#c2c2c2")
            client_data = self.clients_table.item(selected)["values"]
            window.title(f"{client_data[4]}")
            window.resizable(False, False)

            lb = Label(window, text=f"تفاصيل", font=("Dubai", 14, "bold"))
            lb.pack(pady=100)

            window.mainloop()

    def fetch_client_data(self):
        client_selected = self.clients_table.selection()
        client_data = self.clients_table.item(client_selected)["values"]

        self.name.set(client_data[4])
        self.email.set(client_data[2])
        self.gender.set(client_data[1])
        self.address.set(client_data[0])

        # Set Phone with zero
        with sqlite3.connect("clients.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT phone FROM `clients` WHERE id = ?", (client_data[5],))
            client_phone = cur.fetchone()
            self.phone.set(client_phone[0])

    def empty_felids(self):
        self.name.set("")
        self.phone.set("")
        self.email.set("")
        self.gender.set("")
        self.address.set("")


# ============ Run App ============

root = Tk()

ManagementSystem(root)
root.mainloop()
