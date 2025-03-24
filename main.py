from tkinter import *
from tkinter import ttk

# from tkinter import


class Client:
    def __init__(self, root):
        # ============ Main window ============
        self.root = root
        self.root = root.state("zoomed")
        self.root = root.title("إدارة العملاء")
        self.root = root.iconbitmap(r"images\management.ico")
        self.root = root.configure(background="#c2c2c2")
        title = Label(
            root, text="إدارة العملاء", font=("", 14, "bold"), bg="black", fg="white"
        )
        # title.pack(fill=X)

        # ============ Control Panel ============
        style = ttk.Style()
        style.configure("TNotebook.Tab", font=("Dubai", 12))
        control_panel = ttk.Notebook(root)
        control_panel.place(x=1050, y=1)

        control_frame = Frame(
            root, bg="#f2f3f4", bd=2, relief="sunken", width=300, height=700
        )
        control_frame.pack()

        details_frame = Frame(
            root, bg="#f2f3f4", bd=2, relief="sunken", width=300, height=700
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

        id_lb = Label(control_frame, text="Id", **label_options)
        id_lb.pack()
        id_ent = Entry(control_frame, **entry_options)
        id_ent.pack()

        name_lb = Label(control_frame, text="الأسم", **label_options)
        name_lb.pack()
        name_ent = Entry(control_frame, **entry_options)
        name_ent.pack()

        phone_lb = Label(control_frame, text="رقم الهاتف المحمول", **label_options)
        phone_lb.pack()
        phone_ent = Entry(control_frame, **entry_options)
        phone_ent.pack()

        email_lb = Label(control_frame, text="البريد الإلكتروني", **label_options)
        email_lb.pack()
        email_ent = Entry(control_frame, **entry_options)
        email_ent.pack()

        gender_lb = Label(control_frame, text="الجنس", **label_options)
        gender_lb.pack()
        gender_ent = ttk.Combobox(
            control_frame,
            values=("ذكر", "أنثي"),
            font=("Dubai", 12),
            width=23,
            state="readonly",
        )
        gender_ent.pack()

        address_lb = Label(control_frame, text="العنوان", **label_options)
        address_lb.pack()
        address_ent = Entry(control_frame, **entry_options)
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
        add_bt = Button(control_frame, text="إضافة", **bt_options)
        add_bt.pack(pady=10)

        # -- Delete
        delete_title = Label(control_frame, text="حذف عميل", **frame_title_options)
        # delete_title.pack( fill=X)

        delete_id_lb = Label(
            control_frame, text="العميل للحذف Id ادخل ", **label_options
        )
        delete_id_lb.pack()
        delete_id_ent = Entry(control_frame, **entry_options)
        delete_id_ent.pack()

        delete_bt = Button(control_frame, text="حذف", **bt_options)
        delete_bt.pack(pady=10)

        # ============  Search ============
        search_frame = Frame(
            root, bg="#f2f3f4", bd=2, relief="sunken", width=1040, height=60
        )
        search_frame.place(y=2, x=5)
        x = 400
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
            width=10,
            font=("Dubai", 8, "bold"),
            bg="#35f8ae",
            cursor="hand2",
            relief="raised",
            bd=2,
        )
        search_bt.place(x=x - 80, y=10)

        # ============ Show clients ============

        clients_frame = Frame(
            root, bg="white", width=1040, height=630, bd=2, relief="sunken"
        )
        clients_frame.place(x=5, y=70)

        # Configure Treeview
        style.configure("Treeview.Heading", font=("Dubai", 13, "bold"))
        style.configure("Treeview", font=("Dubai", 11, ""))
        style.configure("Treeview", rowheight=35)

        # Create Treeview
        self.clients_table = ttk.Treeview(
            clients_frame,
            columns=("address", "email", "phone", "gender", "name", "id"),
            show="headings",
        )
        self.clients_table.place(x=18, y=0, height=610, width=1018)

        self.clients_table.heading("id", text="Id")
        self.clients_table.heading("name", text="الأسم")
        self.clients_table.heading("gender", text="النوع")
        self.clients_table.heading("phone", text="رقم الهاتف")
        self.clients_table.heading("email", text="البريد الإلكتروني")
        self.clients_table.heading("address", text="العنوان")

        # Format Columns
        self.clients_table.column("id", anchor="center", width=30)
        self.clients_table.column("name", anchor="center", width=180)
        self.clients_table.column("gender", anchor="center", width=60)
        self.clients_table.column("phone", anchor="center", width=150)
        self.clients_table.column("email", anchor="center", width=180)
        self.clients_table.column("address", anchor="center", width=239)

        # Scrollbar
        scroll_x = Scrollbar(
            clients_frame, orient=HORIZONTAL, command=self.clients_table.xview
        )
        scroll_x.place(x=1, y=610, width=1035)

        scroll_y = Scrollbar(
            clients_frame, orient=VERTICAL, command=self.clients_table.yview
        )
        scroll_y.place(x=1, height=610)

        self.clients_table.config(
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set
        )

        # Insert Data
        for i in range(50):
            self.clients_table.insert(
                "",
                "end",
                values=(
                    "مصر, محافظة قنا, مركز فرشوط قرية العسيرات\n",
                    "aaaaaadhmrabee9@.com",
                    f"+962 0779529892",
                    "ذكر",
                    f"ادهم ربيع احمد محمد عثمان",
                    i,
                ),
            )


# ============ Run App ============
root = Tk()

client = Client(root)

root.mainloop()
