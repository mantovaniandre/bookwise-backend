from configuration.database import Session

# created instances
session = Session()


class UserVersionRepository:
    @staticmethod
    def save_user_version_to_database(user_version):
        try:
            session.add(user_version)
            session.commit()
            session.refresh(user_version)
            user_id = user_version.id
            if user_id is not None:
                return True
            else:
                session.rollback()
                return False
        except Exception as e:
            session.rollback()
            raise ValueError(f"Internal data base error: {e}")
        finally:
            session.close()
