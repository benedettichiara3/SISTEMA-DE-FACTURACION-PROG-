from flask import Blueprint, render_template, request
from flask_login import login_required
from models.factura import Factura
from models.cliente import Cliente
from models import db

reportes_bp = Blueprint("reportes", __name__, url_prefix="/reportes")

#reporte de facturas por cliente
@reportes_bp.route("/clientes", methods=["GET", "POST"])
@login_required
def facturas_por_cliente():
    clientes = Cliente.query.all()
    facturas = []

    if request.method == "POST":
        id_cliente = request.form["cliente"]
        facturas = Factura.query.filter_by(id_cliente=id_cliente).all()

    return render_template("reporte_clientes.html", clientes=clientes, facturas=facturas)

#reporte de ventas por período
@reportes_bp.route("/ventas", methods=["GET", "POST"])
@login_required
def ventas_por_periodo():
    facturas = []
    total = 0

    if request.method == "POST":
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]

        facturas = Factura.query.filter(
            Factura.fecha >= fecha_inicio,
            Factura.fecha <= fecha_fin
        ).all()

        total = sum([f.total for f in facturas])

    return render_template("reporte_ventas.html", facturas=facturas, total=total)
