from models import db

class Cliente(db.Model):
    __tablename__ = "clientes"

    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))

    facturas = db.relationship("Factura", backref="cliente", lazy=True)

    def __repr__(self):
        return f"<Cliente {self.nombre}>"
