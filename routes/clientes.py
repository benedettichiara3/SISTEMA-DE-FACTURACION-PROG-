from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.cliente import Cliente
from flask_login import login_required

clientes_bp = Blueprint("clientes", __name__, url_prefix="/clientes")

#listar clientes
@clientes_bp.route("/")
@login_required
def lista_clientes():
    clientes = Cliente.query.all()
    return render_template("clientes.html", clientes=clientes)

#crear cliente
@clientes_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    if request.method == "POST":
        nombre = request.form["nombre"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        email = request.form["email"]

        cliente = Cliente(nombre=nombre, direccion=direccion, telefono=telefono, email=email)
        db.session.add(cliente)
        db.session.commit()
        flash("Cliente creado con éxito")
        return redirect(url_for("clientes.lista_clientes"))

    return render_template("cliente_form.html", accion="Nuevo")

#editar cliente
@clientes_bp.route("/editar/<int:id_cliente>", methods=["GET", "POST"])
@login_required
def editar_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)

    if request.method == "POST":
        cliente.nombre = request.form["nombre"]
        cliente.direccion = request.form["direccion"]
        cliente.telefono = request.form["telefono"]
        cliente.email = request.form["email"]

        db.session.commit()
        flash("Cliente actualizado")
        return redirect(url_for("clientes.lista_clientes"))

    return render_template("cliente_form.html", accion="Editar", cliente=cliente)

#eliminar cliente
@clientes_bp.route("/eliminar/<int:id_cliente>", methods=["POST"])
@login_required
def eliminar_cliente(id_cliente):
    cliente = Cliente.query.get_or_404(id_cliente)
    db.session.delete(cliente)
    db.session.commit()
    flash("Cliente eliminado")
    return redirect(url_for("clientes.lista_clientes"))
