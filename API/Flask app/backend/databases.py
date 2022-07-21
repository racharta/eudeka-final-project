from required import db, randint, datetime


def create_id(for_db:db.Model):  # [DONE]
    code = str(for_db.__tablename__)[0].upper()
    id = code+"".join(
                [str(randint(0,9)) for _ in range(randint(4,9))]
                )
    if for_db.query.filter_by(id=id).all():
        return create_id(for_db)
    else:
        return id


class User(db.Model):  # [DONE]
    id = db.Column(db.String(10), unique=True, primary_key=True)
    avatar = db.Column(db.String(200), nullable=False, default="https://www.svgrepo.com/show/209349/user-avatar.svg")
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    kota = db.Column(db.String(50), nullable=False)
    provinsi = db.Column(db.String(50), nullable=False)

    terakhir_diedit = db.Column(db.DateTime, nullable=False, default=datetime.now())
    is_authenticated = True
    __saldo = 1000000000
    def __repr__(self):
        return f'<{self.id}, {self.username}>'
    def json(self):
        return {"id": self.id,
                "avatar":self.avatar,
                "username": self.username,
                "email": self.email,
                "kota": self.kota,
                "provinsi": self.provinsi}
    def is_active(self):
        return True
    def get_id(self):
        return self.id
    def get_saldo(self):
        return self.__saldo


class Barang(db.Model):  # [DONE]
    id = db.Column(db.String(10), primary_key=True)
    gambar = db.Column(db.String(200), nullable=False, default="https://flyclipart.com/shopping-cart-png-icon-free-download-shopping-cart-icon-png-301449")
    nama = db.Column(db.String(20), nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    stok = db.Column(db.Integer, nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    dari_user = db.Column(db.String(100), nullable=False)
    dari_kota = db.Column(db.String(30), nullable=False)
    berat = db.Column(db.Integer, nullable=False)  # dalam satuan gram 
    deskripsi = db.Column(db.String(300), nullable=False, default="")
    rating = db.Column(db.Float, nullable=False, default=0.)
    banyak_rating = db.Column(db.Integer, nullable=False, default=0)
    yg_sudah_beli = db.Column(db.Integer, nullable=False, default=0)
    terakhir_diedit = db.Column(db.DateTime, nullable=False, default=datetime.now())
    def __repr__(self):
        return f"<id: {self.id} nama:{self.nama}>"
    def json(self):
        return {"id": self.id,
                "nama": self.nama,
                "stok": self.stok,
                "harga": self.harga,
                "deskripsi": self.deskripsi,
                "dari_kota": self.dari_kota,
                "yg_sudah_beli": self.yg_sudah_beli}


class Pesanan(db.Model):  # [DONE]
    id = db.Column(db.String(10), primary_key=True)  # id dari pesanan
    id_barang = db.Column(db.String(10), nullable=False)
    id_pembeli = db.Column(db.String(10), nullable=False)
    banyak = db.Column(db.Integer, nullable=False)
    ongkir = db.Column(db.Integer, nullable=False)
    dari_kota = db.Column(db.String(30), nullable=False)
    ke_kota = db.Column(db.String(30), nullable=False)
    harga_total = db.Column(db.Integer, nullable=False)  # harga termasuk ongkir
    waktu_dibuat = db.Column(db.DateTime, nullable=False) 
    terakhir_diedit = db.Column(db.DateTime, nullable=False, default=datetime.now())
    __status = db.Column(db.String(20), nullable=False, default="belum di bayar")
    def __repr__(self):
        return f"<pesanan: {self.id}, barang:{self.id_pembeli}, dari_user:{self.id_barang}>"
    def json(self):
        return {"id": self.id,
                "id_barang": self.id_barang,
                "id_pembeli": self.id_pembeli,
                "banyak": self.banyak,
                "ongkir": self.ongkir,
                "harga_total": self.harga_total,
                "dari_kota": self.dari_kota,
                "ke_kota": self.ke_kota,
                "waktu_dibuat": str(self.waktu_dibuat),
                "terakhir_diedit": str(self.terakhir_diedit),
                "status": self.get_status()
                }
    def edit(self, **args):
        for k, v in args.items():
            setattr(self, k, v)
        self.terakhir_diedit = datetime.now()
    def get_status(self):
        return self.__status
    def edit_status(self, value):
        self.__status = value
        self.terakhir_diedit = datetime.now()