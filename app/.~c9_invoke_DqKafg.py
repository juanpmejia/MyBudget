from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Paulips'}  # usuario Test fake user
    return render_template('index.html',
                           title='Home',
                           user=user)
                          
@app.route('/registro')
def registro():
    return render_template('registro.html',
                            title='registro')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/base')
    return render_template('login.html', 
                           title='Iniciar Sesión',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
                           
                         