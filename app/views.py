import os
from flask import render_template, redirect, url_for, flash, jsonify, redirect, request, session
from app import app
from .forms import LoginForm

from .validations import *

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Paulips'}  # usuario Test fake user
    return render_template('index.html',
                           title='Home',
                           user=user)
                          
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if(request.method == 'POST'):
        error = None
        print("Hay un post :D")
        if(validRegisterForm(request.form)):
            createUser(request.form)
            status = "Cuenta registrada exitosamente"
        else:
            status = "El email ya fue registrado, prueba con una cuenta de correo diferente"
        print(status)            
        return render_template('registerResult.html',
                            title = 'Registro',
                            status = status)
        
            
            
    return render_template('registro.html',
                            title='Registro')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html', 
                           title='Iniciar Sesión'
                           )

@app.route('/try_login', methods=['GET', 'POST'])
def try_login():
    print("Login requested")
    email = request.args.get("email","",type=str)
    password = request.args.get("password","",type=str)
    if(registeredEmail(email)):
        if(validLogin(email,password)):
            print("Login succesful")
            user = getUser(email)
            ans = "ok"
            session["email"] = email
            session["name"] = user["name"]
            session["gender"] = user["gender"]
            redirect("/lobby")
            print(email,password)
        else:
            print("Invalid password")
            ans = "Contraseña errada"
            
    else:
        print("Invalid email")
        ans = "Email invalido"
    return jsonify(ans=ans)
    
                           

@app.route('/balance')
def balance():
    return render_template('balance.html',
                            title='Balance')


@app.route('/gasto')
def gasto():
    return render_template('gasto.html',
                            title='Ingreso de gasto')                            
                           
                         
@app.route('/crearCategoria')
def crearCategoria():
    return render_template('crearCategoria.html',
                            title='Crear categoría')
                            
@app.route('/lobby')
def lobby():
    if "name" in session:
        return render_template('lobbyUsuario.html',
                                title='Tu lobby',
                                name = session["name"],
                                welcome = "Bienvenido" if session["gender"] == "M" else "Bienvenida")
    else:
        return "Oie ke te paza, porque nos hackeaps D:<"
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")
        
secret_key = os.urandom(24)
print("Ma'h secrety key is ",secret_key)