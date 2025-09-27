from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.producto import Producto
from flask_login import login_required

productos_bp = Blueprint("productos", __name__, url_prefix="/productos")

# Listar productos
@productos_bp.route("/")
@login_required
def lista_productos():
    productos = Producto.query.all()
    return render_template("productos.html", productos=productos)

# Crear producto
@productos_bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    if request.method == "POST":
        descripcion = request.form["descripcion"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])

        producto = Producto(descripcion=descripcion, precio=precio, stock=stock)
        db.session.add(producto)
        db.session.commit()
        flash("Producto creado con éxito")
        return redirect(url_for("productos.lista_productos"))

    return render_template("producto_form.html", accion="Nuevo")

# Editar producto
@productos_bp.route("/editar/<int:id_producto>", methods=["GET", "POST"])
@login_required
def editar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)

    if request.method == "POST":
        producto.descripcion = request.form["descripcion"]
        producto.precio = float(request.form["precio"])
        producto.stock = int(request.form["stock"])

        db.session.commit()
        flash("Producto actualizado")
        return redirect(url_for("productos.lista_productos"))

    return render_template("producto_form.html", accion="Editar", producto=producto)

# Eliminar producto
@productos_bp.route("/eliminar/<int:id_producto>", methods=["POST"])
@login_required
def eliminar_producto(id_producto):
    producto = Producto.query.get_or_404(id_producto)
    db.session.delete(producto)
    db.session.commit()
    flash("Producto eliminado")
    return redirect(url_for("productos.lista_productos"))
