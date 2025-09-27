from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.factura import Factura
from models.cliente import Cliente
from models.producto import Producto
from models.detalle_factura import DetalleFactura
from flask_login import login_required
from datetime import date

facturas_bp = Blueprint("facturas", __name__, url_prefix="/facturas")

#listado de facturas
@facturas_bp.route("/")
@login_required
def lista_facturas():
    facturas = Factura.query.all()
    return render_template("facturas.html", facturas=facturas)

# Crear nueva factura
@facturas_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva_factura():
    clientes = Cliente.query.all()
    productos = Producto.query.all()

    if request.method == "POST":
        id_cliente = int(request.form["cliente"])
        productos_seleccionados = request.form.getlist("producto")
        cantidades = request.form.getlist("cantidad")

        if not productos_seleccionados:
            flash("Debes seleccionar al menos un producto")
            return redirect(url_for("facturas.nueva_factura"))

        # Crear factura
        factura = Factura(id_cliente=id_cliente, fecha=date.today(), total=0.0)
        db.session.add(factura)
        db.session.commit()

        total = 0
        for i, id_producto in enumerate(productos_seleccionados):
            producto = Producto.query.get(int(id_producto))
            cantidad = int(cantidades[i])
            subtotal = producto.precio * cantidad

            detalle = DetalleFactura(
                id_factura=factura.id_factura,
                id_producto=producto.id_producto,
                cantidad=cantidad,
                precio_unitario=producto.precio,
                subtotal=subtotal
            )
            db.session.add(detalle)

            # Actualizar stock
            producto.stock -= cantidad
            total += subtotal

        factura.total = total
        db.session.commit()

        flash("Factura creada con éxito")
        return redirect(url_for("facturas.lista_facturas"))

    return render_template("factura_form.html", clientes=clientes, productos=productos)

# Ver detalle de factura
@facturas_bp.route("/detalle/<int:id_factura>")
@login_required
def detalle_factura(id_factura):
    factura = Factura.query.get_or_404(id_factura)
    detalles = DetalleFactura.query.filter_by(id_factura=id_factura).all()
    return render_template("factura_detalle.html", factura=factura, detalles=detalles)
