from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, ValidationError, Email

from eggList.models.grupo_familiar import GrupoFamiliar
from eggList.models.usuario import Usuario


class GrupoFamiliarForm(FlaskForm):
    familia = StringField('Nombre', validators=[DataRequired(), Length(min=3, max=50)])
    imagen = FileField('Imagen', validators=[FileAllowed(['jpg','jpeg','png', 'webp'])])
    submit = SubmitField('Enviar')

    def validate_familia(self, familia):
        grupo = GrupoFamiliar.query.filter(GrupoFamiliar.nombre_familia == familia.data).first()
        if grupo and grupo.nombre != current_user.grupo_familiar.nombre_familia:
            raise ValidationError("Esa nombre ya existe")


class AgregarUsuarioForm(FlaskForm):
    email_usuario = StringField('Mail', validators=[DataRequired(), Email()])
    submit = SubmitField('Agregar')

    def validar_email_usuario(self, email_usuario):
        user = Usuario.query.filter_by(email_usuario=email_usuario.data)
        if not user or not user.email_confirmed_at:
            raise ValidationError("Ese mail no pertenece a ningun usuario, intente de nuevo")
