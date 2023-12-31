from functools import wraps
from datetime import datetime
from flask import current_app, render_template, url_for
from flask_login import current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy import and_, text
from eggList import db, bcrypt
from eggList.models import Usuario, RolUsuario
from eggList.usuarios.forms import UserForm
from eggList.utils import send_email



def verify_id_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        user_id = s.loads(token)['user_id']
        user = Usuario.query.get(user_id)
    except:
        return None
    return user

def add_role(user:Usuario, role:str):
    rol = RolUsuario.query.filter(RolUsuario.name == role).first()
    if rol:
        user.add_user_role(rol)
        return True
    else:
        return False

def confirm_user(user:Usuario):
    user.email_confirmed_at = datetime.utcnow()
    add_role(user, "Usuario")
    db.session.commit()


def user_roles_required(*roles):
    """Valida que el usuario actual tenga los roles necesarios"""
    def decorator_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated:
                tiene_rol = False
                for rol in roles:
                    tiene_rol = tiene_rol or current_user.has_user_role(rol)
                if tiene_rol:
                    return func(*args, **kwargs)
            return render_template("errores/error_rol.html")
        return wrapper
    return decorator_function

def create_user(register_form: UserForm):
    user: Usuario = get_user_by_email(register_form.email.data)
    if not user:
        password_hash = bcrypt.generate_password_hash(register_form.password.data).decode('utf-8')

        user = Usuario(
            nombre=register_form.nombre.data,
            apellido=register_form.apellido.data,
            email=register_form.email.data,
            telefono=register_form.telefono.data,
            password=password_hash
        )

        db.session.add(user)

    else:
        user.nombre = register_form.nombre.data
        user.apellido = register_form.apellido.data
        user.password = register_form.password.data
        user.telefono = register_form.telefono.data
    send_email(users=[user], title="Creacion de cuenta en EggList",
               body=f"""Usted ha solicitado crear una cuenta en eggList
    Por favor, dirijase al siguiente link si quiere confirmar la cuenta:
    {url_for('usuarios.confirm_register', confirm_token=user.get_id_token(), _external=True)}

    Si no fue usted, por favor, ignore el mensaje
                               """
               )
    db.session.commit()
    return user




def get_user_by_email(email:str):
    return Usuario.query.filter(Usuario.email == email).first()


