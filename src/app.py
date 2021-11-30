from flask import Flask
from flask import render_template, request, redirect, url_for, send_from_directory
from flaskext.mysql import MySQL
from datetime import datetime as dt
import os

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '2589cami' #'25&9c4mi'
app.config['MYSQL_DATABASE_DB'] = 'sistema'

mysql.init_app(app)

@app.route('/userpic/<path:nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(os.path.join('uploads'),nombreFoto)

CARPETA = os.path.join('src/uploads')
app.config['CARPETA'] = CARPETA

@app.route('/')
def index():
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM empleados;"
    cursor.execute(sql)

    empleados = cursor.fetchall()
    
    conn.commit()

    return render_template('empleados/index.html', empleados= empleados)

@app.route('/destroy/<int:id>')
def destroy(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    
    sql = "DELETE FROM `empleados` WHERE id= %s;"
    datos = id
    cursor.execute(sql, datos)

    conn.commit()
    
    return redirect('/')

@app.route('/create')
def create():
    return render_template('empleados/create.html')

@app.route('/update', methods=["POST"])
def update():
    _nombre = request.form("txtNombre")
    _correo = request.form("txtCorreo")
    _foto = request.files("txtFoto")
    id = request.form("txtID")
    
    sql = "UPDATE `empleados` SET `nombre`=%s,`correo`=%s WHERE id=%s;"
    datos = (_nombre ,_correo,id)
    
    conn = mysql.connect()
    cursor = conn.cursor()

    now = dt.now()
    tiempo = now.strftime("%Y%H%M%S")
    if _foto.filename != '':
        newNombreFoto = tiempo + _foto.filename
        _foto.save("src/uploads/"+ newNombreFoto)
        
        sql = "SELECT foto FROM `empleados` WHERE id=%s;"
        datos = id
        cursor.execute(sql, datos)
        
        nombreFoto = cursor.fetchone()[0]

        sql = "UPDATE `empleados` SET foto=%s WHERE id=%s;"
        datos = (newNombreFoto,id)
        cursor.execute(sql, datos)
        
        conn.commit()
    
    cursor.execute(sql, datos)

    conn.commit()
    
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    conn = mysql.connect()
    cursor = conn.cursor()

    sql = "SELECT * FROM empleados WHERE id=%s;"
    datos = (id)
    cursor.execute(sql, datos)

    empleados = cursor.fetchall()
    
    conn.commit()

    return render_template('empleados/edit.html', empleados= empleados)

@app.route('/store', methods=["POST"])
def store():
    _nombre = request.form("txtNombre")
    _correo = request.form("txtCorreo")
    _foto = request.files("txtFoto")
    
    conn = mysql.connect()
    cursor = conn.cursor()

    now = dt.now()
    tiempo = now.strftime("%Y%H%M%S")
    if _foto.filename != '':
        newNombreFoto = tiempo + _foto.filename
        _foto.save("src/uploads/"+ newNombreFoto)
    
    sql = "INSERT INTO `empleados` (`id`,`nombre`,`correo`,`foto`) VALUES (NULL, %s, %s, %s);"
    datos = (_nombre ,_correo, newNombreFoto)
    cursor.execute(sql, datos)

    conn.commit()
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)