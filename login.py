from customtkinter import *
from PIL import Image
from tkinter import messagebox

class Login:
    def __init__(self, root):

        self.center_window(root, 600, 350)
        self.root = root
        self.root.title("Login")
        self.root.iconbitmap(r"images\management.ico")
        self.check_var = False

        # main frame in center of window
        fr_width, fr_height = 500, 300
        a, b = (600 // 2) - (500 // 2), (350 // 2) - (300 // 2)  # x,y value
        self.main_frame = CTkFrame(
            self.root, width=fr_width, height=fr_height, corner_radius=50
        )
        self.main_frame.place(x=a, y=b)

        img = Image.open(r"images\account.png")
        ctk_img = CTkImage(dark_image=img, light_image=img, size=(100, 100))
        login_img = CTkLabel(self.main_frame, image=ctk_img, text="")
        login_img.place(x=190, y=10)

        # x,y place value
        x, y = 100, 130
        # Username entry
        self.username_ent = CTkEntry(
            self.main_frame,
            width=300,
            height=40,
            font=("Arial Rounded MT", 18),
            placeholder_text="Enter your username",
        )
        self.username_ent.place(x=x, y=y)

        # Password entry
        self.password_ent = CTkEntry(
            self.main_frame,
            width=300,
            height=40,
            font=("Arial Rounded MT", 18),
            show="*",
            placeholder_text="Enter your password",
        )
        self.password_ent.place(x=x, y=y + 60)

        # Login button
        login_bt = CTkButton(
            self.main_frame,
            text="Login",
            font=("Arial Rounded MT", 20),
            height=40,
            command=self.check,
        )
        login_bt.place(x=x + 70, y=y + 120)

        # Press enter to login
        self.root.bind("<Return>",lambda event:self.check())

    def center_window(self, window, window_width, window_height):
        """
        Function to set window in center of screen
        """
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    
    def check(self):
        if self.username_ent.get() == "admin" and self.password_ent.get() == "admin":
            self.check_var = True
            self.root.destroy()
            
        else:
            messagebox.showerror("Error", "Incorrect username or password")


