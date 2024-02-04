from eggList import db


class Ciudad(db.Model):
    __tablename__ = "ciudades"

    cod_postal = db.Column(db.Integer(), primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    id_provincia = db.Column(db.Integer(),db.ForeignKey("provincias.id",
                                                        ondelete="CASCADE",
                                                        onupdate = "CASCADE"),nullable = False)
    provincia = db.relationship("Provincia", back_populates="ciudades", )
    supermercados = db.relationship("Supermercado", back_populates="ciudad")
