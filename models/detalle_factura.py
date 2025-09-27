from models import db

class DetalleFactura(db.Model):
    __tablename__ = "detalle_factura"

    id_detalle = db.Column(db.Integer, primary_key=True)
    id_factura = db.Column(db.Integer, db.ForeignKey("facturas.id_factura"), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey("productos.id_producto"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<DetalleFactura {self.id_detalle} - Factura {self.id_factura}>"
