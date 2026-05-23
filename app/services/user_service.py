from app.models import db, User
from email_validator import validate_email, EmailNotValidError

class UserService:
    @staticmethod
    def register_user(email, password, name=None):
        """Registers a new user if the email is not already taken and is valid."""
        if len(password) < 6:
            return False, "Senha deve ter pelo menos 6 caracteres"

        try:
            # Validate email format without DNS check for speed and test compatibility
            validate_email(email, check_deliverability=False)
        except EmailNotValidError:
            return False, "Formato de email inválido"

        if User.query.filter_by(email=email).first():
            return False, "Usuário já cadastrado"
        
        new_user = User(email=email, name=name)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        return True, new_user

    @staticmethod
    def authenticate_user(email, password):
        """Authenticates a user by email and password."""
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            return True, user
        else:
            return False, "Credenciais inválidas"

    @staticmethod
    def update_password(user_id, new_password):
        """Updates the password for a given user."""
        if len(new_password) < 6:
            return False, "Senha deve ter pelo menos 6 caracteres"

        user = db.session.get(User, user_id)
        if not user:
            return False, "Usuário não encontrado"
        
        user.set_password(new_password)
        db.session.commit()
        return True, "Senha atualizada"

    @staticmethod
    def delete_user(user_id):
        """Deletes a user and their associated data."""
        user = db.session.get(User, user_id)
        if not user:
            return False, "Usuário não encontrado"
        
        db.session.delete(user)
        db.session.commit()
        return True, "Usuário excluído"
