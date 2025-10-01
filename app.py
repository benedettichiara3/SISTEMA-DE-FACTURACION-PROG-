from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user
from config import Config
from models import db
from models.user import User
from models.cliente import Cliente
from models.producto import Producto
from models.factura import Factura
from flask_login import logout_user


from routes.clientes import clientes_bp
from routes.productos import productos_bp
from routes.facturas import facturas_bp
from routes.reportes import reportes_bp

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)


login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(clientes_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(facturas_bp)
app.register_blueprint(reportes_bp)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]  # en el form el input se llama username, pero corresponde al email
        password = request.form["password"]

        usuario = User.query.filter_by(email=email).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)  
            return redirect(url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos")
            return render_template("login.html")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nombre = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            flash("Las contraseñas no coinciden")
            return render_template("registro.html")

        usuario = User.query.filter_by(email=email).first()
        if usuario:
            flash("El usuario ya existe")
            return render_template("registro.html")

       
        nuevo_usuario = User(nombre=nombre, email=email)
        nuevo_usuario.set_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario registrado con éxito. Inicia sesión.")
        return redirect(url_for("login"))

    return render_template("registro.html")


@app.route("/dashboard")
@login_required
def dashboard():
    clientes_count = Cliente.query.count()
    productos_count = Producto.query.count()
    facturas_count = Factura.query.count()
    return render_template(
        "dashboard.html",
        clientes_count=clientes_count,
        productos_count=productos_count,
        facturas_count=facturas_count
    )


@app.route("/logout")
@login_required
def logout():
    logout_user() 
    flash("Sesión cerrada correctamente")
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
