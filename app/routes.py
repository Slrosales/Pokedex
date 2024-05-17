from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, current_user, logout_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User
from app import login_manager

@app.route('/')
def index():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
   if request.method == 'POST':
       username = request.form['username']
       email = request.form['email']  # Asegúrate de incluir el email en tu formulario.
       password = request.form['password']

       # Verificar que el username o email no existan ya en la base de datos
       user_exists = User.query.filter((User.username == username) | (User.email == email)).first() is not None

       if user_exists:
           flash('El nombre de usuario o correo electrónico ya existe.')
           return redirect(url_for('register'))

       # Crear una nueva instancia de User
       new_user = User(
           username=username,
           email=email,
           password_hash=generate_password_hash(password, method='sha256')  # Encriptar la contraseña
       )

       # Agregar el nuevo usuario a la base de datos
       db.session.add(new_user)
       db.session.commit()

       flash('Registro exitoso. Por favor, inicia sesión.')
       return redirect(url_for('login'))

   return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Si el usuario ya está autenticado, redirigir a la página principal
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # Manejar la solicitud POST
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=request.form.get('remember'))  
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Credenciales inválidas. Por favor intente de nuevo.')

    # Mostrar el formulario de inicio de sesión para una solicitud GET
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
