"""
yang belum beres:
1. Main Frame di bagian dashboard (isinya list barang)
2. halaman pesanan
3. halaman bayar pesanan / konfirmasi pesanan
4. lihat password sekilas di login/signup page
"""
import io, json
from tkinter import *
from PIL import Image, ImageTk
import requests as req
import yaml

window = Tk()
window.resizable(0,0)

HEIGHT = window.winfo_screenheight()
WIDTH = window.winfo_screenwidth()
LOGIN = False
URL = "http://127.0.0.1:5000/"

with open("language.yaml", "r") as f:
    text = yaml.full_load(f)

class Page:
    bg = ""
    bg_nav = "#09baf4"
    bg_main = "white"
    font_entry = ["Arial", 16]
    title = "Page"
    width, height = WIDTH, HEIGHT
    def __init__(self, window:Tk):
        self.window = window
        self.window.title(self.title)
        self.window.geometry(
            f"{self.width}x{self.height}+{(WIDTH-self.width)//2} \
            +{(HEIGHT-self.height)//2}"
            )
        msg_label = Label(self.window, text="", bg=self.bg_nav)
        self.window.update()
        self.window.tkraise()
        print(f"In Page {self.__class__.__name__}")
    def change_text(self, label:Label, text=""):
        label.config(text=text)
    def ungrid_all(self):
        for w in self.window.grid_slaves():
            w.grid_remove()
    def switch_to(self, to):
        self.ungrid_all()
        to(self.window)


class Auth(Page):
    url = f"{URL}api/login/"
    data = {"username": "", "email": "", "password": ""}
    submit_msg = 'login'
    width, height = 360, 450
    def __init__(self, window:Tk):
        super().__init__(window)
        self.menu = Menu(self.window, bg='#9c9c9c')
        self.window.config(menu=self.menu)

        global img
        img = Image.open("img/vector.png").resize((200, 200))
        img = ImageTk.PhotoImage(img)

        # auth_label = Label(self.window, text="Login", font=('Arial', 32))
        vector = Label(self.window, image=img)
        auth_frame = Frame(self.window, borderwidth=2)
        for k in self.data.keys():
            setattr(self, f"{k}_label", Label(auth_frame, text=k))
            setattr(self, 
                    f"{k}_entry", 
                    Entry(auth_frame, font=("Arial", 10), width=50, 
                            show="*" if k=='password' else '')
                    )
        submit_btn = Button(auth_frame, text=self.submit_msg, command=self.post)
        
        # ===================== GRIDING ===================
        # auth_label.grid(row=0, column=0, columnspan=3)
        vector.grid(row=1, column=0, pady=5,
                    rowspan=2, columnspan=3,)
        auth_frame.grid(row=3, column=0, pady=10)
        n = 3
        for k in self.data.keys():
            getattr(self, f"{k}_label").grid(row=n, column=0)
            n += 1
            getattr(self, f"{k}_entry").grid(row=n, column=0)
            n +=1
        submit_btn.grid(row=n+1, column=0, pady=10)
        self.window.update()

    def post(self):
        try:
            if not LOGIN:
                for k in self.data.keys():
                    self.data[k] = getattr(self, f"{k}_entry").get()
                res = req.post(self.url, json=self.data)
                if res.status_code == 200:
                    print("login succes")
                    self.window.config(menu="")
                    self.switch_to(Dashboard)
                    globals()['LOGIN'] = True
                else:
                    print(res.content)
                    self.msg_label.config(text = res.content, font=("Arial BOLD", 12))
                    self.msg_label.after(5000, lambda: self.msg_label.config(text=""))
            else:
                print("Anda sudah login, tidak perlu login lagi")
                self.window.config(menu="")
                self.switch_to(Dashboard)
        except Exception as e:
            print(f"{e.__class__.__name__}: {e.args[0]}")
            self.msg_label.config(text = e.__class__.__name__, font=("Arial BOLD", 12))
            self.msg_label.after(5000, lambda: self.msg_label.config(text=""))


class LoginByEmail(Auth):
    title = "Login by Email"
    data = {"email": "", "password": ""}
    def __init__(self, window:Tk):
        super().__init__(window)
        self.menu.add_command(label="Login by Username", 
                              command=lambda: self.switch_to(LoginByUsername))
        self.menu.add_separator()
        self.menu.add_command(label="Create Account", 
                              command=lambda: self.switch_to(SignUp))
        

class LoginByUsername(Auth):
    title = "Login by Username"
    data = {"username": "", "password": ""}
    def __init__(self, window:Tk):
        super().__init__(window)
        self.menu.add_command(label="Login by Email",
                              command=lambda: self.switch_to(LoginByEmail))
        self.menu.add_separator()
        self.menu.add_command(label="Create Account",
                              command=lambda: self.switch_to(SignUp))
        

class SignUp(Auth):
    title = "Create Account"
    data = {"username": "", "email": "", "password": ""}
    url = f"{URL}api/signup/"
    submit_msg = "Sign up"
    def __init__(self, window:Tk):
        super().__init__(window)
        self.menu.add_command(label="Login by Email",
                              command=lambda: self.switch_to(LoginByEmail))
        self.menu.add_command(label="Login by Username",
                              command=lambda: self.switch_to(LoginByUsername))


class Dashboard(Page):
    title = "Dashboard"
    def __init__(self, window:Tk):
        super().__init__(window)
        # ================ icon ===================
        global search_icon, keranjang_icon
        img1 = Image.open("img/search-icon.png").resize((30,30))
        img2 = Image.open("img/keranjang.png").resize((30,30))
        search_icon = ImageTk.PhotoImage(img1)
        keranjang_icon = ImageTk.PhotoImage(img2)

        # ================ Navbar Area ===================
        # =========== navbar frame ===========
        navbar_frame = Frame(self.window, bg=self.bg_nav)
        # ============ Label Toko ============
        label_toko = Label(navbar_frame, text="Toko Onlen", 
                            font=("Arial", 32), bg=self.bg_nav)
        # =========== Search Area ============
        search_frame = Frame(navbar_frame, bg='white')
        search_entry = Entry(search_frame, font=self.font_entry, 
                                width=60, borderwidth=0)
        search_button = Button(search_frame, bg=self.bg_nav, image=search_icon, 
                                borderwidth=0, height=30, width=30)
        # ============= User Area =============
        keranjang_button = Button(navbar_frame, image=keranjang_icon)
        user_button = Button(navbar_frame, 
                            text="Login/SignUp" if not LOGIN else "my account", 
                            command=lambda :self.switch_to(LoginByEmail) \
                                if not LOGIN else self.switch_to())

        # ================= Main Area ===================
        main_frame = Frame(self.window, bg=self.bg_main)
        try:
            all_barang = req.get(f"{URL}api/cari/barang/all/all").content
            for i in json.loads(all_barang):
                pass
        except Exception as e:
            self.msg_label.config(text=e.__class__.__name__, 
                                  font=("Arial BOLD", 16),
                                  bg=self.bg_nav, fg='black')
            self.msg_label.update()
            self.msg_label.grid(row=0, column=0)
            self.msg_label.after(5000, 
                                 lambda: self.msg_label.grid_remove())
            self.msg_label.update()
            # print(e.args[0])
            print(e.__class__.__name__)
        
        # =================== GRIDING =========================
        navbar_frame.grid(row=1, column=0, ipadx=WIDTH)
        label_toko.grid(row=0, column=0, padx=20, pady=5)
        search_frame.grid(row=0, column=1, ipadx=2, padx=30, pady=10)
        search_entry.grid(row=0, column=0, ipady=5, padx=7)
        search_button.grid(row=0, column=1, padx=2, pady=3)
        keranjang_button.grid(row=0, column=2, pady=5, padx=10)
        user_button.grid(row=0, column=3)


class UserInfo(Page):
    def __init__(self, window: Tk, **args):
        super().__init__(window)
        global img
        # url_avatar = args['gambar']
        # res = req.get(url_avatar)
        # img = Image.open(io.BytesIO(res))
        nav_frame = Frame(self.window)
        
        info_frame = Frame(self.window)
        my_pesanan_frame = Frame(self.window)
        my_produk_frame = Frame(self.window)
        password_frame = Frame(self.window)


class DeskripsiBarang(Page):
    def __init__(self, window: Tk, **args):
        super().__init__(window)
        self.window.size()


class PagePesanan(Page):
    def __init__(self, window: Tk):
        super().__init__(window)
    

if __name__ == "__main__":
    Dashboard(window)
    window.mainloop()
