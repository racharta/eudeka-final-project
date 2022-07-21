# import modul
import json
import os

# open file json
file1 = open("produk.json", "r")

# save produk.json to variabel
data = json.load(file1)
produk = list(data.keys())
stok = {}
for p in produk: 
    stok[p] = data[p]["stok"]

# function cetak produk
# format -> 1. produk a     : harga
#           2. produl wxyz  : harga 
#           3. produk abc   : harga
def print_produk():
    # cari nama terpanjang
    p2 = produk.copy()
    p2.sort(key=lambda x: len(x))
    length = len(p2[-1])
    # cara2 : length = max(p2, key=len)

    # print daftar produk
    print("="*16 + " List produk " + "="*16, "\n")
    for n, p in enumerate(produk, start=1):
        print(f"{n}. {p:<{length}} = {data[p]['harga']} {'(stok habis)' if not stok[p] else ''}")
    print("0. untuk keluar")
    print("="*45)

def print_pesanan(pesanannya):
    print("\n########## Detail Pesanan ##########")
    # print("Detail Pesanan")
    for p in pesanannya.keys():
        print("----------------------------------")
        print("Menu   : ", p)
        print("Jumlah : ", pesanannya[p])
        print("Harga  : Rp", data[p]["harga"] * pesanannya[p])
        print("----------------------------------")  # 34 tanda '-'
    print("Total  : Rp", total)
    print("####################################")  # 36 tanda '#'

# looping 
# get input nama, nomer produk, jumlah, uang yg dimiliki
# end if input -> 0 or exit or e or E
pesanan = {}
total = 0
nama = input("masukkan nama anda: ",)
while True:
    try:
        os.system("cls")
        print("**********************************************")
        print(f"selamat datang {nama} di rumah makan santuy")
        print("silahkan pilih menu yang akan di beli")
        print("**********************************************")
        
        print_produk()

        nomer = int(input("pilih nomer produk: ",))
        yang_dibeli = produk[nomer - 1] 
        if nomer == 0: break  
        if stok[yang_dibeli] == 0: continue

        jumlah = int(input("berapa banyak? ",))
        if jumlah < 1: continue

        if stok[yang_dibeli] < jumlah:
            print(f"maaf stok {yang_dibeli} kami hanya tinggal: {stok[yang_dibeli]}")
            tetap = input("ingin tetap membeli dengan stok yang tersisa? (Y/N): ",)
            if tetap == "Y":
                pesanan[yang_dibeli] = jumlah = stok[yang_dibeli]
            else:
                jumlah = 0
                continue
        else:
            if yang_dibeli in pesanan.keys():
                pesanan[yang_dibeli] += jumlah
            else:
                pesanan[yang_dibeli] = jumlah

        stok[yang_dibeli] -= jumlah
        total += data[yang_dibeli]["harga"] * jumlah
        print_pesanan(pesanan)

        lanjut = input("\nmau pesan lagi (Y/N)? ",)
        if lanjut.upper() == "N":
            break
    except Exception as e:
        print(e.args[0])
        continue

# proses pesanan
if total and nomer:
    os.system("cls")
    print("      Proses Pembayaran Pesanan")
    print_pesanan(pesanan)

    uang = int(input("masukkan uang anda: ",))
    print("**************************************")
    if uang >= total:  # ketika uang pembeli cukup
        for p in pesanan.keys(): 
            data[p]["stok"] -= pesanan[p]
        with open("produk.json", "w") as f:
            f.write(json.dumps(data, indent=4))
            
        print("Transaksi berhasil")
        if uang-total == 0: 
            print("Uang anda pas") 
        else: 
            print(f"kembalian anda adalah {uang-total}")
    else:  # ketika uang pembeli kurang
        print("Ooops uang yang anda miliki \ntidak cukup untuk membeli pesanan")
        print("coba lain kali")

print("**************************************")
print("Terima kasih telah mengunjungi warung kami :)")
print("Silahkan datang kembali\n")