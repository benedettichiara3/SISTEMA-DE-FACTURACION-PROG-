from models import db

class Factura(db.Model):
    __tablename__ = "facturas"

    id_factura = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey("clientes.id_cliente"), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, default=0.0)

    detalles = db.relationship("DetalleFactura", backref="factura", lazy=True)

    def __repr__(self):
        return f"<Factura {self.id_factura} - Cliente {self.id_cliente}>"
