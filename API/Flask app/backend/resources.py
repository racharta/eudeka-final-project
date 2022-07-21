from databases import *
from required import *
from ongkir import *

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):  # [DONE]
    try:
        return User.query.filter_by(id=id).one()
    except Exception as e:
        print(e)
        return

def clear_none(args:dict):  # [DONE]
    return {k:v for k, v in args.items() if not v is None}

class EditUser(Resource):  # [DONE]
    parser = RequestParser()
    parser.add_argument("username", type=str, help="id user")
    parser.add_argument("email", type=str, help="email user")
    parser.add_argument("password", type=str, help="password user")

    @login_required
    def get(self):  # ambil data current user [DONE]
        try:
            return jsonify(**current_user.json())
        except Exception as e:
            return jsonify(msg=e.__class__.__name__)

    @login_required
    def put(self):  # edit user [DONE]
        args = self.parser.parse_args()
        user = current_user
        for k, v in args.items():
            if not v is None and args['password'] == user.password:
                print(k, v)
                setattr(user, k, v)
        db.session.commit()
        return jsonify(msg="success update data", data={**args})

    @login_required
    def delete(self):  # delete user [DONE]
        args = self.parser.parse_args()
        args = clear_none(args)
        try:
            user = current_user
            if args["password"] == user.password:
                db.session.delete(user)
                db.session.commit()
                txt = f"deleted:\n {user} \nby: {request.remote_addr}"
                return jsonify(msg=txt)
            else:
                return jsonify(msg="Wrong password")
        except Exception as e:
            return jsonify(msg=e.__class__.__name__)


class SignUp(Resource):  # [DONE]
    parser = RequestParser()
    parser.add_argument("username", type=str, help="id user")
    parser.add_argument("email", type=str, help="email user")
    parser.add_argument("password", type=str, help="password user")
    parser.add_argument("kota", type=str, help="asal kota mana...")
    parser.add_argument("provinsi", type=str, help="asal kota mana...")
    def post(self):
        args = self.parser.parse_args()
        id = create_id(User)
        args.update({"id":id})
        args = {k: v for k, v in args.items() if v is not None}
        if city_is_available(args['kota']):
            try:
                user = User(**args)
                db.session.add(user)
                db.session.commit()
                return jsonify(msg="Sign Up success", user_id=args['id'])
            except Exception as e:
                if e.__class__.__name__ == "IntegrityError":
                    return jsonify(msg="user is exist", user_id=None)
                else:
                    return jsonify(msg=f"{e.__class__.__name__}: {e}", user_id=None)
        else:
            return jsonify(msg="Error, city is not found")


class Login(Resource):  # [DONE]
    def post(self):
        parser = RequestParser()
        parser.add_argument("username", type=str)
        parser.add_argument("email", type=str)
        parser.add_argument("password", type=str, required=True)
        args = parser.parse_args()
        args = clear_none(args)
        try:
            user = User.query.filter_by(**args).one()
            if args.get("password") == user.password:
                login_user(user)
                print(f"logged in {user.username} from {request.remote_addr}")
                return jsonify(msg="login success", user_id=user.id)
            else:
                return jsonify(msg="Wrong password", user_id=None)
        except Exception as e:  # user not found!
            return jsonify(msg=f"{e.__class__.__name__}: {e}", user_id=None)


class Logout(Resource):  # [DONE]
    @login_required
    def post(self):
        logout_user()
        return jsonify(msg='Logout Success')




class CheckOngkir(Resource):
    def get(self, from_, to, weight, courier='jne'):
        cost = get_cost(
            get_city(from_)['city_id'],
            get_city(to)['city_id'],
            weight,
            courier
            )
        return cost


class EditBarang(Resource):  # [DONE]
    parser = RequestParser()
    parser.add_argument("nama", type=str, help="nama barang")
    parser.add_argument("stok", type=int, help="stok barang")
    parser.add_argument("harga", type=int, help="harga barang")
    parser.add_argument("deskripsi", type=str, help="deskripsi barang")

    @login_required
    def get(self):  # list current user (user yg login) [DONE]
        args = self.parser.parse_args()
        args = clear_none(args)
        try:
            all_barang = Barang.query.filter_by(dari_user=current_user.id, **args).all()
            data = [i.json() for i in all_barang]
            return jsonify(msg="success", data=data)
        except Exception as e:
            return jsonify(msg=e.__class__.__name__, data=None)

    @login_required
    def post(self):  # tambah barang  [DONE]
        self.parser.add_argument("kategori", type=str, help="kategori barang", required=True)
        self.parser.add_argument("gambar")
        args = self.parser.parse_args()
        args.update({'id': create_id(Barang)})
        args.update({'dari_user': current_user.id})
        args.update({'dari_kota': current_user.dari_kota})
        args = clear_none(args)
        if city_is_available(args['dari_kota']):
            try:
                barang = Barang(**args)
                db.session.add(barang)
                db.session.commit()
                return jsonify(msg="tambah barang berhasil",
                               id_barang=barang.id)
            except Exception as e:
                print(e.args[0])
                print(e.__class__.__name__)
                return jsonify(msg=e.__class__.__name__, barang_id=None)
        else:
            return jsonify(msg="city is not found")

    @login_required
    def delete(self):  # hapus barang [DONE]
        args = self.parser.parse_args()
        args = clear_none(args)
        try:
            barang = Barang.query.filter_by(**args).one()
            if barang.dari_user == current_user.id:
                db.session.delete(barang)
                db.session.commit()
                print(f"deleted:\n{barang}by: {request.remote_addr}")
                return jsonify(msg=f"success deleted <{barang.nama}>")
            else:
                print(f"cannot delete {barang.nama} because is not yours")
                return jsonify(f"cannot delete {barang.nama} because is not yours")
        except Exception as e:
            print(e)
            return jsonify(msg=e.__class__.__name__)

    @login_required
    def put(self):  # update barang (ubah deskripsi, harga atau yg lain-lain)
        self.parser.add_argument("id", type=str, help="id barang anda", required=True)
        args = self.parser.parse_args()
        args = clear_none(args)
        try:
            barang = Barang.query.filter_by(id=args.get('id'), dari_user=current_user.id).one()
            for k, v in args.items():
                setattr(barang, k, v)
            db.session.commit()
            return jsonify(msg=f"success edit barang {barang}")
        except Exception as e:
            print(e)
            return jsonify(msg=e.__class__.__name__)


class CariBarang(Resource):  # [DONE]
    """
    cari barang berdasarkan kategori dan nama
    """
    def get(self):
        barang = []
        if request.args:
            for k, v in dict(request.args).items():
                if k != 'count':
                    barang += Barang.query.filter(getattr(Barang, k).contains(v)).all()
        else:
            for i in Barang.query.all():
                barang += [i.json()]
        data = [barang.json() for barang in barang]
        try:
            count = int(request.args.get("count"))
            data = data[:count]
        except Exception:
            pass
        return data



class Keranjang(Resource):  # [DONE]
    @login_required
    def get(self):  # [DONE]
        args = request.args
        if not args:
            my_pesanan = Pesanan.query.filter_by(id_pembeli=current_user.id)
            data = [i.json() for i in my_pesanan]
            return data

    @login_required
    def post(self):  # [DONE]
        parser = RequestParser()
        parser.add_argument("id_barang", type=str, help="id dari barang")
        parser.add_argument("banyak", type=int)
        args = parser.parse_args()
        try:
            barang = Barang.query.filter_by(id=args['id_barang']).one()
            args['ongkir'] = get_cost(barang.dari_kota, current_user.dari_kota, barang.berat)
            if pesanan:= Pesanan.query.filter_by(
                            id_pembeli=current_user.id,
                            id_barang=args["id_barang"]
                         ).all():  # ketika barang udh ada di pesanan
                pesanan = pesanan[0]
                if barang.stok >= args['banyak']:
                    pesanan.banyak += args['banyak']
                    pesanan.harga_total = pesanan.banyak * barang.harga + args['ongkir']
                    pesanan.edit()
                    db.session.commit()
                    return jsonify(msg=f'sukses menambahkan <{barang.nama}>\
                                         ke keranjang <{current_user.username}>')
                else:
                    return jsonify(msg="stok barang tidak cukup")
            else:  # kalau barang belum ada di pesanan/keranjang
                args['id'] = create_id(Pesanan)
                args['id_pembeli'] = current_user.id
                args['dari_kota'] = barang.dari_kota
                args['ke_kota'] = current_user.dari_kota
                args['harga_total'] = args['banyak'] * barang.harga + args['ongkir']
                args['waktu_dibuat'] = datetime.now()
                if barang.stok >= args.get('banyak'):
                    pesanan = Pesanan(**args)
                    db.session.add(pesanan)
                    db.session.commit()
                    return jsonify(msg=f'sukses menambahkan <{barang.nama}>\
                                         ke keranjang <{current_user.username}>')
                else:
                    return jsonify(msg=f'stok barang tidak cukup')
        except Exception as e:
            return jsonify(msg=f"{e.__class__.__name__}:{e.args[0]}")

    @login_required
    def put(self):
        if id := request.args.get('id'):
            parser = RequestParser()
            parser.add_argument('banyak', type=int, help="")
            parser.add_argument('ke_kota', type=str, help="kota tujuan pengiriman barang")
            args = parser.parse_args()
            args = clear_none(args)
            pesanan = Pesanan.query.filter_by(id=id).one()
            for k, v in args.items():
                setattr(pesanan, k, v)
            barang = Barang.query.filter_by(id=pesanan.id_barang).one()
            pesanan.edit(harga_total=pesanan.banyak * barang.harga + pesanan.ongkir)
            db.session.commit()
            return jsonify(msg=f"success edit pesanan {pesanan}")
        else:
            return jsonify(msg="tolong masukkan id pesananmu")


class BayarPesanan(Resource):  # [DONE]
    @login_required
    def post(self, id):
        try:
            pesanan = Pesanan.query.filter_by(id=id).one()
            if pesanan.get_status() == "belum di bayar":
                pesanan.edit_status("sudah di bayar")
                db.session.commit()
                return jsonify(msg="pembayaran berhasil")
        except Exception as e:
            return jsonify(msg=f"error {e.__class__.__name__}: {e}")


class KonfirmasiPesanan(Resource):  # kalau paket udh nyampe [DONE]
    @login_required
    def post(self, id):
        try:
            pesanan = Pesanan.query.filter_by(id=id).one()
            if pesanan.get_status() == "sudah di bayar":
                pesanan.edit_status("selesai")
                db.session.commit()
                return jsonify(msg=f"success konfirmasi pesanan {pesanan}")
        except Exception as e:
            return jsonify(msg=f"{e.__class__.__name__}:\n{e}")

