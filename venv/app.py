from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import werkzeug
import pytz
import numpy as np
import pandas as pd
from werkzeug.utils import secure_filename
import bcrypt 
import os
import optimal
from io import StringIO
import csv
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from passlib.hash import bcrypt
from sqlalchemy.orm import scoped_session,sessionmaker

app = Flask(__name__)
app.secret_key = "LOgin21"

app.config['UPLOAD_FOLDER'] = 'uploads' #konfigurasi nama folder upload
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/eclatdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inisisiasi db
db = SQLAlchemy(app)
#pembuatan model Transaction
class User(db.Model): #membuat kelas
    __tablename__= "users" 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255)) 
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    role = db.Column(db.String(255))

class Transaction(db.Model): #membuat kelas
    __tablename__= "transactions" 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255)) 
    dataset = db.Column(db.String(255))
    rule = db.Column(db.String(255))
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.timezone('Asia/Jakarta')))
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))

@app.route('/')
def home() :
    return render_template("home.html")

@app.route('/admin', methods=['POST', 'GET'])
def admin() :
    return render_template("login.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password").encode('utf-8')
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if bcrypt.verify(password, user.password):
                session['name'] = user.name
                session['username'] = user.username
                session['id'] = user.id
                if user.role=='admin':
                    return redirect(url_for('halamanadmin'))
                else :
                    return redirect(url_for('home'))
            else:
                flash("Gagal, Username dan Password Tidak Cocok", "danger")
                return redirect(url_for('login'))
        else:
            flash("User Tidak Ditemukan, Silahkan Register", "danger")
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/register', methods=['POST', 'GET'])
def register(): 
    if request.method == 'GET':
        return render_template('register.html')
    else :
        name = request.form['name']
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hash(password)
        role = 'user'

        new_user = User(name=name, username=username, password=hash_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash("Anda berhasil registrasi, silahkan login","success")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/tampil')
def tampil():
    if 'username' in session:
        transactions= Transaction.query.all()
        return render_template("tampil.html", transactions=transactions)
    else:
        return redirect(url_for('home'))

@app.route('/upload', methods = ['POST'])
def tambah():
        file = request.files['file']
        if file:
            file_name = secure_filename(file.filename) #ambil jika spasi otomatis underscore
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name) #ambil lokasi file
            exiting_transaction = Transaction.query.filter_by(dataset=file_name,id_user=session['id']).first()
            if exiting_transaction: #ini buat pesan error
                flash("Data Sudah Ada, Silahkan lihat Menu Riwayat", "danger")
                return redirect(url_for('tampil'))
            file.save(file_path) #nyimpen file csv
            rule_df = optimal.hitung_eclatku(file_path) #jalanin modelnya
            rule_file_name = f'{os.path.splitext(file_name)[0]}_rule.csv' #hilangin ekstensi + rule
            rule_file_path = os.path.join(app.config['UPLOAD_FOLDER'], rule_file_name)
            rule_df.to_csv(rule_file_path) #csv disimpen ke sini

            transaction = Transaction(
                name = os.path.splitext(file_name)[0],
                dataset = file_name,
                rule = rule_file_name,
                id_user = session['id']
            )
            db.session.add(transaction)
            db.session.commit()

            return redirect(url_for('view',id=transaction.id, id_user=transaction.id_user))
        else:
            return render_template('tampil.html', error="Gagal memproses file CSV.")

@app.route('/halamanadmin')
def halamanadmin() :
    users = User.query.filter(User.role != "admin").all()#mengambil database user
    return render_template('halamanadmin.html', users=users)  

@app.route('/riwayat')
def riwayat() :
    if 'id' in session:
        transactions = Transaction.query.filter_by(id_user=session['id']).all() #mengambil semua data dari tabel transaksi
        return render_template('riwayat.html', transactions=transactions)
    else:
        return redirect(url_for('home'))

@app.route('/delete/<int:id>')
def delete(id):
    transactions = Transaction.query.filter_by(id=id).first()
    db.session.delete(transactions)
    db.session.commit()
    return redirect(url_for('riwayat')) 

@app.route('/deleteuser/<int:id>')
def deleteuser(id):
    users = User.query.filter_by(id=id).first()
    db.session.delete(users)
    db.session.commit()
    return redirect(url_for('halamanadmin')) 

@app.route('/view/<int:id>')
def view(id):
    transaction = Transaction.query.filter_by(id=id).first() #ambil id
    rule_file_name = transaction.rule
    rule_file_path = os.path.join(app.config['UPLOAD_FOLDER'], rule_file_name) #ambil path result
    rule_df=pd.read_csv(rule_file_path) 
    return render_template('view.html', tables=[rule_df.to_html(classes='data')],titles=rule_df.columns.values, transaction=transaction)

@app.route('/download/<int:transaction_id>', methods=['POST'])
def download(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    rule_file_name = transaction.rule
    rule_file_path = os.path.join(app.config['UPLOAD_FOLDER'], rule_file_name)

    return send_file(rule_file_path,
                     mimetype='text/csv',
                     as_attachment=True,
                     download_name=rule_file_name)


@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('home')) 

#debug sudah dideklarasikan pada .env

    