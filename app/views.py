import os
import locale
from flask import render_template, redirect, url_for, flash, jsonify, redirect, request, session
from app import app
from .forms import LoginForm

from .validations import *


locale.setlocale(locale.LC_ALL, 'es_CO.utf8')



@app.route('/')
@app.route('/index')
def index():
    if "name" in session:
        return redirect("/lobby")
    else:
        return render_template('index.html',
                           title='Home'
                           )
                          
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
                           
                         
@app.route('/crearCategoria', methods = ['GET', 'POST'])
def crearCategoria():
    if "name" in session:
        if (request.method == 'POST'):
            print("Hice un post :D")
            error = None
            if (validCategoryForm(request.form,session['email'])):
                createCategory(request.form, session['email'])
                status = "Categoria agregada satisfactoriamente"
                buttonText = "Volver al lobby"
                link = "/lobby"
            else:
                status = "La categoría ya habia sido creada anteriormente. Escoge un nombre nuevo por favor."
                buttonText = "Volver a Crear Categoría"
                link = "/crearCategoria"
            return render_template('categoryCreationResult.html',
                                title='Crear categoría',
                                status = status,
                                buttonText = buttonText,
                                link = link)
        else:
            return render_template('crearCategoria.html',
                                title='Crear categoría')
    else:
        return redirect("/accessdenied")
        
                            
@app.route('/lobby')
def lobby():
    if "name" in session:
        categories = getCategories(session['email'])
        for c in categories:
            c["totalCost"] = locale.currency(c["totalCost"], grouping = True)
        user = getUser(session['email'])
        return render_template('lobbyUsuario.html',
                                title='Tu lobby',
                                categories = categories,
                                name = session["name"],
                                budget = locale.currency(user["budget"], grouping = True),
                                welcome = "Bienvenido" if session["gender"] == "M" else "Bienvenida")
    else:
        return redirect("/accessdenied")
        
        
@app.route('/deposit', methods = ['GET', 'POST'])
def deposit():
    if "name" in session:
        if(request.method =='GET'):
            destinations = [{"name" : session["email"]}]
            return render_template('deposit.html',
                                    title='Ingresos',
                                    destinations = destinations,
                                    name = "Name")#session["name"])
        elif(request.method =='POST'):
            if(request.form["destination"] == session["email"]):
                createIncome(request.form, userEmail=request.form["destination"])
            else:
                createIncome(request.form, groupId=request.form["destination"])
            return redirect("/lobby")
    else:
        return redirect("/accessdenied")
        

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")
    
@app.route('/accessdenied')
def accessDenied():
    return render_template('accessDenied.html',
        title='Acceso denegado')

app.secret_key = os.urandom(24)
print("Ma'h secrety key is",app.secret_key)


@app.route('/expenseHist')
def expenseHist():
    if('name in session'):
        category = request.args.get("category","",type=str)
        expenses = readExpenses(category, session['email'])
        return render_template('expenseHistory.html',
                                expenses = expenses,
                                title='Historial de gasto')                            
                           