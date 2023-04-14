from configuration.database import Session
from model.user import User

# created instances
session = Session()


class LoginRepository:
    @staticmethod
    def get_user_by_email(email_login_upper):
        try:
            user = session.query(User).filter_by(email=email_login_upper).first()
            if user:
                return user
            else:
                session.rollback()
                raise ValueError(f"Email not found")
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal data base error: {e}")
        finally:
            session.close()

