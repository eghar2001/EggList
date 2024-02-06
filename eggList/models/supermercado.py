from eggList import db


class Supermercado(db.Model):
    __tablename__ = "supermercados"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(70), nullable=False, unique=False)

    cod_postal = db.Column(db.Integer(),db.ForeignKey("ciudades.cod_postal"),nullable = False)
    ciudad = db.Relationship("Ciudad", back_populates = "supermercados")

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.nombre} ({self.ciudad.nombre}, {self.ciudad.provincia.nombre})"
