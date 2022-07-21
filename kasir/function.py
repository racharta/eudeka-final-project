import os

class Produk:
    def __init__(self, data:dict) -> None:
        self.data = data
    
    def index(self, index):
        return list(self.data.keys())[index]

    def harga(self, name:str):
        return self.data[name]['harga']
    
    def stok(self, name:str):
        return self.data[name]["stok"]

    def kurangi_stok(self, nama, jumlah):
        self.data[nama]['stok'] -= jumlah

    def __str__(self):
        str_ = ""
        panjang = len(max(self.data.keys(), key=len))
        for nomer, produk in enumerate(self.data.keys(), start=1):
            habis = '(stok habis)' if not self.stok(produk) else ''
            str_ += f"{nomer}. {produk:<{panjang}} = {self.data[produk]['harga']} {habis}" + "\n"
        return str_

class Pesan:
    """
    format:
    {
        <nama>: {
            "jumlah": <jumlah>,
            "harga satuan": <harga>
        }
    }
    """
    def __init__(self):
        self.pesanan = {}

    def tambah_pesanan(self, menu, harga, jumlah):
        if self.pesanan.get(menu):
            self.pesanan[menu]['jumlah'] += jumlah
        else:
            self.pesanan[menu]['jumlah'] = jumlah
        self.pesanan[menu]['harga satuan'] = harga
    
    def harga(self, item:str):
        for k, v in self.pesanan.items():
            if item == k:
                return v["harga satuan"]

    def total_harga(self):
        j = 0
        for nama, banyak in self.pesanan.items():
            j += self.harga(nama) * banyak
        return j
    
    def __str__(self):
        str_ = "\n########## Detail Pesanan ##########\n"
        for menu, desc in self.pesanan.items():
            str_ += "----------------------------------\n"
            str_ += f"Menu    : {menu}\n" 
            str_ += f"Jumlah  : {desc['jumlah']}\n"
            str_ += f"Harga   : Rp{self.harga(menu)}\n"
            str_ += f"subtotal: Rp{self.harga(menu)*desc['jumlah']}\n"
            str_ += "----------------------------------\n"  # 34 tanda '-'
        str_ += f"Total  : Rp{self.jumlah()}\n"
        str_ += "####################################\n"
        return str_

def print_banner(nama):
    print("**********************************************")
    print(f"selamat datang {nama} di rumah makan santuy")
    print("silahkan pilih menu yang akan di beli")
    print("**********************************************")

def clear():
    os.system("cls" if (os.name == "nt") else "clear")