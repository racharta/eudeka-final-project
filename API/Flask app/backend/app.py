from resources import *

# ROUTES
api.add_resource(EditUser, "/api/user/")
api.add_resource(Login, "/api/login/")
api.add_resource(Logout, "/api/logout/")
api.add_resource(SignUp, "/api/signup/")
api.add_resource(EditBarang, "/api/barang/")
api.add_resource(CariBarang, "/api/cari/barang/")
api.add_resource(Keranjang, "/api/pesanan/")
api.add_resource(BayarPesanan, "/api/bayar/<string:id>")
api.add_resource(KonfirmasiPesanan, "/api/konfirmasi/<string:id>")

@app.route("/")
def halo():
    return "halo user"


