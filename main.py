from customtkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3


# Connect to the database
with sqlite3.connect("persons.db") as conn:
    cur = conn.cursor()

    # Create Table
    cur.execute(
        """CREATE TABLE IF NOT EXISTS persons (
    address TEXT,
    gender TEXT,
    email TEXT UNIQUE,
    phone TEXT,
    name TEXT,
    id INTEGER PRIMARY KEY
    )"""
    )
    conn.commit()


class ManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام إدارة")
        self.root.state("zoomed")
        # self.root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        self.root.resizable(False, False)
        self.root.iconbitmap(r"images\management.ico")

        # ============ Variables ============
        self.name = StringVar()
        self.gender = StringVar()
        self.phone = StringVar()
        self.email = StringVar()
        self.address = StringVar()
        self.person_id = StringVar()
        self.search_var = StringVar()

        # ============ Control panel ============
        self.control_frame = CTkFrame(
            self.root, height=670, width=360, corner_radius=20
        )
        self.control_frame.place(x=1000, y=30)

        # person Details Section
        details_label = CTkLabel(
            self.control_frame, text="بيانات العميل", font=("Dubai", 20, "bold")
        )
        details_label.place(x=125, y=10)

        # x,y place value
        x = 35
        lb_x = 160
        y = 30
        # Default font
        ent_font = ("Dubai", 16)
        lb_font = ("Dubai", 18, "bold")

        # Name Field
        CTkLabel(self.control_frame, text="الأسم", font=lb_font).place(x=lb_x, y=y + 20)
        self.name_entry = CTkEntry(
            self.control_frame,
            textvariable=self.name,
            width=300,
            font=ent_font,
            justify="center",
            fg_color=("gray81", "#333333"),
        )
        self.name_entry.place(x=x, y=y + 60)

        # Gender Field
        CTkLabel(self.control_frame, text="النوع", font=lb_font).place(
            x=lb_x, y=y + 110
        )
        self.gender_combo = CTkComboBox(
            self.control_frame,
            values=["ذكر", "أنثى"],
            variable=self.gender,
            font=ent_font,
            width=300,
            state="readonly",
            justify="center",
            fg_color=("gray81", "#333333"),
        )
        self.gender_combo.place(x=x, y=y + 150)

        # Phone Field
        CTkLabel(self.control_frame, text="رقم الهاتف", font=lb_font).place(
            x=lb_x - 15, y=y + 200
        )
        self.phone_entry = CTkEntry(
            self.control_frame,
            textvariable=self.phone,
            width=300,
            font=ent_font,
            justify="center",
            fg_color=("gray81", "#333333"),
        )
        self.phone_entry.place(x=x, y=y + 240)

        # Email Field
        CTkLabel(self.control_frame, text="البريد الإلكتروني", font=lb_font).place(
            x=lb_x - 30, y=y + 290
        )
        self.email_entry = CTkEntry(
            self.control_frame,
            textvariable=self.email,
            width=300,
            font=ent_font,
            justify="center",
            fg_color=("gray81", "#333333"),
        )
        self.email_entry.place(x=x, y=y + 330)

        # Address Field
        CTkLabel(self.control_frame, text="العنوان", font=lb_font).place(
            x=lb_x, y=y + 380
        )
        self.address_entry = CTkEntry(
            self.control_frame,
            textvariable=self.address,
            width=300,
            font=ent_font,
            justify="center",
            fg_color=("gray81", "#333333"),
        )
        self.address_entry.place(x=x, y=y + 420)

        # ================= Buttons ================= #
        # x,y place value
        x = 110
        y = 510
        # Default font
        ent_font = ("Dubai", 16)
        bt_font = ("Dubai", 16, "bold")

        # Add Button
        self.add_btn = CTkButton(
            self.control_frame,
            text="إضافة",
            command=self.add_person,
            width=150,
            height=40,
            fg_color="#2e8b57",
            hover_color="#3cb371",
            font=bt_font,
        )
        self.add_btn.place(x=x, y=y)

        # Update Button
        self.update_btn = CTkButton(
            self.control_frame,
            text="تحديث",
            command=self.update_person,
            width=150,
            height=40,
            font=bt_font,
        )
        self.update_btn.place(x=x, y=y + 45)

        # Clear Button
        self.clear_btn = CTkButton(
            self.control_frame,
            text="إفراغ الحقول",
            command=self.empty_felids,
            width=150,
            height=40,
            fg_color="#d9534f",
            hover_color="#ff6b6b",
            font=bt_font,
        )
        self.clear_btn.place(x=x, y=y + 90)

        # ================= Menubar ================= #
        menubar = CTkFrame(
            root,
            fg_color=("gray81", "#333333"),
            height=26,
            width=root.winfo_screenwidth(),
            corner_radius=0,
        )
        menubar.place(x=0)

        # --- Options ---
        self.options_bt = tk.Menubutton(
            menubar, text="خيارات", relief="flat", bg="#333333", fg="white"
        )
        self.options_bt.place(x=1)

        self.options = tk.Menu(self.options_bt, tearoff=False)
        self.options_bt["menu"] = self.options

        # Reset
        self.options.add_cascade(label="إعادة تعيين", command="ss")

        # --- Sittings ---

        self.sittings_bt = tk.Menubutton(
            menubar, text="الإعدادات", relief="flat", bg="#333333", fg="white"
        )
        self.sittings_bt.place(x=50)

        # Sittings menu
        self.sittings = tk.Menu(self.sittings_bt, tearoff=False)
        self.sittings_bt["menu"] = self.sittings

        # Appearance menu
        self.appearance = tk.Menu(self.sittings, tearoff=False)
        self.appearance.add_cascade(label="فاتح", command=self.light_mode)
        self.appearance.add_cascade(label="داكن", command=self.dark_mode)
        self.sittings.add_cascade(label="المظهر", menu=self.appearance)

        # ============ Popup menu ============
        # --- Menu click
        self.right_click_menu = tk.Menu(root, tearoff=0)
        self.right_click_menu.add_command(label="تعديل", command=self.fetch_person_data)
        self.right_click_menu.add_command(label="حذف", command=self.delete_person)

        # --- Top Frame --- #
        self.top_frame = CTkFrame(self.root, height=65, width=980, corner_radius=20)
        self.top_frame.place(x=10, y=30)

        # -- Search Frame
        self.search_ent = CTkEntry(
            self.top_frame,
            width=400,
            justify="center",
            font=("Dubai", 14),
            textvariable=self.search_var,
            fg_color=("gray81", "#333333"),
        )
        self.search_ent.place(x=400, y=10)

        self.search_bt = CTkButton(
            self.top_frame, font=("Dubai", 14), text="بحث", command=self.search
        )
        self.search_bt.place(x=258, y=10)

        # ==================== Persons Table ==================== #
        self.table_frame = CTkFrame(root, width=980, height=600, corner_radius=0)
        self.table_frame.place(x=10, y=100)

        self.info_frame = CTkFrame(
            self.table_frame, height=25, width=980, corner_radius=0
        )
        self.info_frame.place(x=0, y=575)

        # Create persons table
        self.persons_table = ttk.Treeview(
            self.table_frame,
            columns=("address", "gender", "email", "phone", "name", "id"),
            show="headings",
        )
        self.persons_table.place(x=0, y=0, height=560, width=965)

        # Call function to show persons
        self.shows_persons()

        # -- Configure Treeview colors
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(
            "Treeview.Heading",
            font=("Dubai", 13, "bold"),
            background="#2b2b2b",
            foreground="white",
        )
        self.style.configure(
            "Treeview",
            font=("Dubai", 13),
            rowheight=35,
            background="#333333",
            fieldbackground="#333333",
            foreground="white",
        )

        self.style.map("Treeview", background=[("selected", "#1f6aa5")])  # Select color

        # Set color depending on the appearance of the system
        if get_appearance_mode() == "Light":
            self.light_mode()

        # -- Table heads
        self.persons_table.heading("id", text="Id")
        self.persons_table.heading("name", text="الأسم")
        self.persons_table.heading("phone", text="رقم الهاتف")
        self.persons_table.heading("email", text="البريد الإلكتروني")
        self.persons_table.heading("gender", text="النوع")
        self.persons_table.heading("address", text="العنوان")

        # Format Columns
        self.persons_table.column("id", anchor="center", width=30)
        self.persons_table.column("name", anchor="center", width=180)
        self.persons_table.column("gender", anchor="center", width=60)
        self.persons_table.column("phone", anchor="center", width=150)
        self.persons_table.column("email", anchor="center", width=180)
        self.persons_table.column("address", anchor="center", width=239)

        # Scrollbar
        scroll_x = CTkScrollbar(
            self.table_frame,
            width=968,
            orientation=HORIZONTAL,
            command=self.persons_table.xview,
        )
        scroll_x.place(x=0, y=560)

        scroll_y = CTkScrollbar(
            self.table_frame, height=570, command=self.persons_table.yview
        )
        scroll_y.place(x=965, y=0)

        self.persons_table.configure(
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )

        # ==================== Events ==================== #
        # -- Persons table events
        self.persons_table.bind("<Button-3>", self.right_click)
        self.persons_table.bind("<Double-1>", self.person_window)

    # ==================== Functions ==================== #
    def empty_felids(self):
        self.name.set("")
        self.phone.set("")
        self.email.set("")
        self.gender.set("")
        self.address.set("")

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

    def right_click(self, event):
        item = self.persons_table.identify_row(event.y)
        if item:
            self.persons_table.selection_set(item)
            self.right_click_menu.tk_popup(event.x_root, event.y_root)  # عرض القائمة

    def dark_mode(self):
        self.options_bt.configure(bg="#333333", fg="white")
        self.sittings_bt.configure(bg="#333333", fg="white")

        self.style.configure(
            "Treeview.Heading",
            background="#2b2b2b",
            foreground="white",
        )
        self.style.configure(
            "Treeview",
            background="#333333",
            fieldbackground="#333333",
            foreground="white",
        )
        set_appearance_mode("dark")

    def light_mode(self):
        self.options_bt.configure(bg="gray81", fg="black")
        self.sittings_bt.configure(bg="gray81", fg="black")
        self.style.configure(
            "Treeview",
            background="gray81",
            foreground="black",
            fieldbackground="gray81",
        )
        self.style.configure(
            "Treeview.Heading", background="gray81", foreground="black"
        )
        set_appearance_mode("light")

    def add_person(self):
        if self.felids_not_empty():
            try:
                with sqlite3.connect("persons.db") as conn:
                    cur = conn.cursor()

                    cur.execute(
                        f"""INSERT INTO `persons` (address,gender,email,phone,name) VALUES(
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

        self.shows_persons()

    def delete_person(self):
        cursor_row = self.persons_table.selection()
        person_id_to_del = self.persons_table.item(cursor_row)["values"][5]

        if messagebox.askquestion(title="حذف عميل", message="حذف العميل") == "yes":
            with sqlite3.connect("persons.db") as conn:
                cur = conn.cursor()
                cur.execute("DELETE FROM `persons` WHERE id = ?", (person_id_to_del,))
                conn.commit()
            self.shows_persons()

    def update_person(self):
        cursor_row = self.persons_table.selection()
        self.selected_person_id = self.persons_table.item(cursor_row)["values"]

        if self.selected_person_id:
            with sqlite3.connect("persons.db") as conn:  #
                cur = conn.cursor()
                cur.execute(
                    "UPDATE `persons` SET address = ?, email = ?, phone = ?, gender = ?, name = ? WHERE id = ?",
                    (
                        self.address.get().strip(),
                        self.email.get().strip(),
                        self.phone.get().strip(),
                        self.gender.get().strip(),
                        self.name.get().strip(),
                        self.selected_person_id[5],
                    ),
                )
                conn.commit()
            self.shows_persons()
            self.empty_felids()
            messagebox.showinfo(title="تحديث", message="تم تحديث بيانات العميل بنجاح")

    def shows_persons(self):

        with sqlite3.connect("persons.db") as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM `persons`")
            rows = cur.fetchall()

            # Show persons count in search frame
            persons_count = len(rows)
            count_lb = CTkLabel(
                self.info_frame,
                text=f"Count: {persons_count}",
                font=("", 14),
                fg_color=(f"gray81", "#333333"),
            )
            count_lb.place(x=10)

        # Show persons in treeview
        self.persons_table.delete(*self.persons_table.get_children())
        for row in rows:
            self.persons_table.insert("", "end", values=row)
            conn.commit()

    def search(self):

        with sqlite3.connect("persons.db") as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT * FROM `persons` 
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

            # Show persons count in search frame
            persons_count = len(rows)
            count_lb = CTkLabel(
                self.info_frame,
                text=f"Count: {persons_count}",
                font=("", 14),
                fg_color=(f"gray81", "#333333"),
            )
            count_lb.place(x=10)

        # Show persons in treeview
        self.persons_table.delete(*self.persons_table.get_children())
        for row in rows:
            # print(row)
            self.persons_table.insert("", "end", values=row)
            conn.commit()

    def person_window(self, event):
        selected = self.persons_table.selection()
        if selected:
            person_data = self.persons_table.item(selected)["values"]

            self.window = CTkToplevel(self.root)
            self.window.iconbitmap(r"images\management.ico")
            self.window.title(f"تفاصيل العميل: {person_data[4]}")
            self.window.geometry("400x400")
            self.window.resizable(False, False)

            # person details frame
            details_frame = CTkFrame(self.window, corner_radius=10)
            details_frame.pack(fill="both", expand=True, padx=20, pady=20)

            # person info labels
            CTkLabel(
                details_frame, text="معلومات العميل", font=("Dubai", 18, "bold")
            ).pack(pady=(20, 30))

            title_ls = [
                " :الأسم",
                " :الهاتف",
                " :البريد",
                " :النوع",
                " :العنوان",
                " :المعرف",
            ]
            a = 80
            b = 4
            for label_text in title_ls:
                l1 = CTkLabel(details_frame, text=label_text, font=("Dubai", 16))
                l1.place(x=250, y=a)
                l2 = CTkLabel(details_frame, text=person_data[b], font=("Dubai", 16))
                l2.place(x=50, y=a)
                a += 30
                b -= 1

    def fetch_person_data(self):
        person_selected = self.persons_table.selection()
        person_data = self.persons_table.item(person_selected)["values"]

        self.name.set(person_data[4])
        self.email.set(person_data[2])
        self.gender.set(person_data[1])
        self.address.set(person_data[0])

        # Set Phone with zero
        with sqlite3.connect("persons.db") as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT phone FROM `persons` WHERE id = ?", (person_data[5],))
            person_phone = cur.fetchone()
            self.phone.set(person_phone[0])


# ========== Run the App ========== #
if __name__ == "__main__":
    root = CTk()
    set_appearance_mode("system")
    print(get_appearance_mode())
    ManagementSystem(root)
    root.mainloop()
