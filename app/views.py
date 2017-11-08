import os
import locale
from flask import render_template, redirect, url_for, flash, jsonify, redirect, request, session
from app import app
from .forms import LoginForm
from bson.json_util import dumps
from .validations import *


locale.setlocale(locale.LC_ALL, 'en_US.utf8')



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
        print("Hay un post:D")
        if(validRegisterForm(request.form)):
            createUser(request.form)
            sendRegistrationEmail(request.form)
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

@app.route('/getUsers')
def geUsers():
    startingWith = request.args.get("term","",type=str)
    ans = []
    if(startingWith):
        print("buscando usuarios que empiecen por",startingWith)
        data = getUsersStartingWith(startingWith)
        for d in data:
            ans.append({"label" : d["email"], "value" : d["email"]})
    print(ans)
    return dumps(ans)
                           

@app.route('/balance')
def balance():
    if('name' in session):
        groupId = request.args.get("groupId","",type=str)
        if(not groupId):
            categories = getCategories(session['email'])
            entity = getUser(session['email'])
            entityType = "usuario"
            print(categories)
        else:
            categories = getCategories(groupId = groupId)
            entity = readGroupById(groupId)
            entityType = "grupo "+entity['subject']
        return render_template('balance.html',
                                categories = categories,
                                entity = entity,
                                title='Balance')
    else:
        return redirect("/accesdenied")

@app.route('/gasto', methods = ['GET', 'POST'])
def gasto():
    if('name' in session):
        if(request.method == 'GET'):
            groupId = request.args.get("groupId", None, type=str)
            if(groupId):
                categories = getCategories(groupId = groupId)
            else:
                categories = getCategories(session['email'])
            return render_template('gasto.html',
                                    categories = categories,
                                    title='Ingreso de gasto')
        elif(request.method == 'POST'):
            groupId = request.args.get("groupId", None, type=str)
            userEmail = session['email'] if not groupId else None
            print("Estan tratando de registrar gasto con form", request.form)
            if(validExpense(request.form,userEmail, groupId)):
                print("CREEARE GASTO")
                if(groupId):
                    createExpense(request.form,groupId = groupId)
                    url = "/lobbyGroup?groupId="+groupId
                else:
                    createExpense(request.form,session['email'])
                    url = "/lobby"
                print("CREE GASTO")
            else:
                url = "/lobby"
                print("gasto no valido")
            return redirect(url)
    else:
        return redirect("/accessdenied")
                           
                         
@app.route('/crearCategoria', methods = ['GET', 'POST'])
def crearCategoria():
    if "name" in session:
        if (request.method == 'POST'):
            if("groupId" in request.args.keys()):
                groupId = request.args.get("groupId","",type=str)
            else:
                groupId = None
            print(request.args)
            print("Hice un post :D")
            error = None
            if (validCategoryForm(request.form,session['email'], groupId)):
                if(groupId):
                    createCategory(request.form, None, groupId)
                else:
                    createCategory(request.form, session['email'])
                status = "Categoria agregada satisfactoriamente."
                buttonText = "Volver al lobby"
                if(not groupId):
                    link = "/lobby"
                else:
                    link = "/lobbyGroup?groupId="+groupId
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
        groups = readGroups(session['email'])
        return render_template('lobbyUsuario.html',
                                title='Tu lobby',
                                groups = groups,
                                categories = categories,
                                name = session["name"],
                                budget = locale.currency(user["budget"], grouping = True),
                                incomesTotal = locale.currency(user["incomesTotal"], grouping = True),
                                expensesTotal = locale.currency(user["expensesTotal"], grouping = True),
                                welcome = "Bienvenido" if session["gender"] == "M" else "Bienvenida")
    else:
        return redirect("/accessdenied")
        
        
@app.route('/deposit', methods = ['GET', 'POST'])
def deposit():
    if "name" in session:
        if(request.method =='GET'):
            groupId = request.args.get("groupId", "", type=str)
            if(groupId):
                defaultSelect = groupId
            else:
                defaultSelect = session['email']
            groups = readGroups(session['email'])
            groups = [{"name" : group["subject"], "id" : str(group["_id"])} for group in groups]
            destinations = [ {"name" : session["email"], "id" : session["email"]} ] + groups
            print(defaultSelect)
            return render_template('deposit.html',
                                    title='Ingresos',
                                    destinations = destinations,
                                    defaultSelect = defaultSelect,
                                    name = "Name")#session["name"])
        elif(request.method =='POST'):
            if(request.form["destination"] == session["email"]):
                url = "/lobby"
                createIncome(request.form, userEmail=request.form["destination"])
            else:
                url = "/lobbyGroup?groupId="+request.form["destination"]
                createIncome(request.form, groupId=request.form["destination"])
            return redirect(url)
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




@app.route('/expenseHist')
def expenseHist():
    if('name' in session):
        category = request.args.get("category","",type=str)
        if(not "groupId" in request.args.keys()):
            expenses = readExpenses(category, session['email'])[::-1]
            for expense in expenses:
                expense['value'] = locale.currency(expense['value'], grouping = True)
                                        
        else:
            groupId = request.args.get("groupId", "", type=str)
            expenses = readExpenses(category,groupId=groupId)[::-1]
            for expense in expenses:
                expense['value'] = locale.currency(expense['value'], grouping = True)
            
        return render_template('expenseHistory.html',
                                    expenses = expenses,
                                    title='Historial de gasto')

@app.route('/incomeHist')
def incomeHist():
    if('name' in session):
        if(not "groupId" in request.args.keys()):
            incomes = readIncomes(session['email'])[::-1]
            for income in incomes:
                income['value'] = locale.currency(income['value'], grouping = True)
                
        else:
            
            groupId = request.args.get("groupId", "", type=str)
            incomes = readIncomes(groupId=groupId)[::-1]
            print(incomes)
            for income in incomes:
                income['value'] = locale.currency(income['value'], grouping = True)
                
        return render_template('incomeHistory.html',
                                incomes = incomes,
                                title='Historial de ingresos')
    else:
        return redirect("/accessdenied")
        
@app.route('/createColabBudget', methods = ['GET', 'POST'])
def colabBudget():
    if('name' in session):
        if(request.method == 'GET'):
            return render_template('colabBudgetCreation.html', 
                                   title='Crear presupuesto grupal'
                                   )
        elif(request.method == 'POST'):
            if(validGroup(session['email'], request.form)):
                createGroup(session['email'], request.form)
                status = "El grupo "+request.form['subject']+" ha sido creado satisfactoriamente."
            else:
                status = "El grupo "+request.form['subject']+" ya existia. Por favor, selecciona un nombre distinto."
            return render_template('colabResult.html',
                                        status = status)
    else:
        return redirect("/accessdenied")
                           
@app.route('/lobbyGroup')
def lobbyGroup():
    if('name' in session):
        groupId = request.args.get("groupId","",type=str)
        if(checkUserInGroup(groupId, session['email'])):
            group = readGroupById(groupId)
            categories = getCategories(groupId = groupId)
            for c in categories:
                c["totalCost"] = locale.currency(c["totalCost"], grouping = True)
            group['budget'] = locale.currency(group['budget'], grouping = True)
            group['incomesTotal'] = locale.currency(group['incomesTotal'], grouping = True)
            group['expensesTotal'] = locale.currency(group['expensesTotal'], grouping = True)
            print(categories)
            return render_template('lobbyGroup.html',
                                    group = group,
                                    categories = categories,
                                    title='Lobby grupal')
        else:
            return redirect("/accessdenied")
    else:
        return redirect('/accessdenied')

@app.route('/memberList')
def memberList():
    if('name' in session):
        print("ajsdhaiusd")
        groupId = request.args.get("groupId", "", type=str)
        members = getMembers(groupId)[::-1]
        print(members,groupId,"memberlist")
        return render_template('memberList.html',
                                members = members,
                                title='Lista de miembros de '+readGroupById(groupId)["subject"])
    else:
        return redirect("/accessdenied")

print(app.secret_key, "llave secreta")
if(app.secret_key == "key"):       
    app.secret_key = os.urandom(24)
    #app.secret_key  = "debug"
    print("Ma'h secrety key is",app.secret_key)