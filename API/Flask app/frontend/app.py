from flask import Flask, flash, redirect, render_template, request, url_for
from time import sleep
import requests as req
import os, json


# url_backend = "https://api-hasban-olshop.herokuapp.com/"
url_backend = "http://127.0.0.1:5000/"
app = Flask("front end")
app.secret_key = "halo orang saya juga orang"


def get_barang(nama="", kategori=""):
    res = req.get(url_backend+f"?nama={nama}")
    return res.json()


def cek_login():
    res = req.get(url_backend+"api/user/")
    if res.status_code == 200 and res.content:
        return True
    else:
        return False

@app.route('/', methods=["GET", "POST"])
def welcome():
    message = ""
    login_status = cek_login()
    if request.method == "POST":
        print(request.form['search'])
    elif request.method == "GET":
        message = request.args.get('message')
    return render_template("index.html", data="", message=message, login=login_status)
    

@app.route("/login", methods = ['GET', 'POST'])
def login():
    # return_url = "http://localhost:5000/"
    return_url = "/"
    required = ['email', 'password']
    if request.method == "GET":
        return render_template("auth.html", len=len(required), data=required, action="login")
    elif request.method == "POST":
        data = request.form
        n_url = url_backend+"api/login/"
        res =  req.post(n_url, 
                        json={'email': data['email'], 
                              'password': data['password']
                             })
        data_res = json.loads(res.content)
        if data_res['user_id']:
            print(f"SUCCESS LOGIN {data_res['user_id']} FROM {request.remote_addr}")
            return redirect(url_for('welcome', message="Login Success"))
        else:
            return redirect(url_for('login', message='Error'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    return_url = "/"
    required = ['username', 'email', 'password', 'city', 'province']
    if request.method == "GET":
        return render_template("auth.html", len=len(required), data=required, action="signup")
    elif request.method == "POST":
        try:
            data = request.form
            n_url = url_backend+"api/signup/"
            res =  req.post(n_url, json={
                    'email': data['email'], 
                    'password': data['password'], 
                    'username': data['username'], 
                    'kota': data['city'],
                    'provinsi': data['province']})
            data_res = json.loads(res.content)
            print(data_res)
            if data_res['user_id']:
                print(f"SUCCESS SIGNUP {data_res['user_id']} FROM {request.remote_addr}")
                return redirect(url_for('login', message="signup success"))
            else:
                return redirect(url_for('signup', message="error when signup"))
        except Exception as e:
            return redirect(url_for('signup', message=str(e.args)))

@app.route('/user/settings')
def user():
    return "halaman user"
    
@app.route("/keranjang")
def keranjang():
    return render_template("pesanan.html")

