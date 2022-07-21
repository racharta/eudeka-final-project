# import modul
import json
from function import *

# open file json
file_ = open("produk.json", "r")

# save produk.json to variabel
data = json.load(file_)
produk = Produk(data)

# looping 
# get input nama, nomer produk, jumlah
# end looping if input -> 0 or exit or e or E
MESSAGE_ERROR = ""
pesanan = Pesan()
nama = input("masukkan nama anda: ",)
print_banner(nama)
while True:
    try:
        clear()
        print(MESSAGE_ERROR, "\n")
        print(produk)

        nomer = int(input("pilih nomer produk: ",))
        yang_dibeli = produk.index(nomer - 1) 
        if nomer == 0: 
            break  

        if produk.stok(yang_dibeli) == 0:
            MESSAGE_ERROR = "maaf stok habis, silahkan pilih yang lain\n" 
            continue

        jumlah = int(input("berapa banyak? ",))
        if jumlah < 1:
            MESSAGE_ERROR = "pesan setidaknya 1 buah" 
            continue

        if produk.stok(yang_dibeli) < jumlah:
            print(f"maaf stok {yang_dibeli} kami hanya tinggal: {produk.stok(yang_dibeli)}")
            tetap = input("ingin tetap membeli dengan stok yang tersisa? (Y/N): ",)
            if tetap == "Y":
                jumlah = produk.stok(yang_dibeli)
            else:
                jumlah = 0
                continue
        
        pesanan.tambah_pesanan(yang_dibeli, produk.harga(yang_dibeli), jumlah)
        produk.kurangi_stok(jumlah)
        
        print(pesanan)

        lanjut = input("\nmau pesan lagi (Y/N)? ",)
        if lanjut.upper() == "N":
            break

    except Exception as e:
        MESSAGE_ERROR = e.args[0]
        continue

# proses pesanan
total = pesanan.total_harga()
if total and nomer:
    clear()
    print("      Proses Pembayaran Pesanan")
    
    print(pesanan)

    uang = int(input("masukkan uang anda: ",))
    print("**************************************")
    if uang >= total:  # ketika uang pembeli cukup

        with open("produk.json", "w") as f:
            f.write(json.dumps(data, indent=4))
            
        print("Transaksi berhasil")
        if uang - total == 0: 
            print("Uang anda pas") 
        else: 
            print(f"kembalian anda adalah {uang - total}")
    else:  # ketika uang pembeli kurang
        print("Ooops uang yang anda miliki \ntidak cukup untuk membeli pesanan")
        print("coba lain kali")

print("**************************************")
print("Terima kasih telah mengunjungi warung kami :)")
print("Silahkan datang kembali\n")