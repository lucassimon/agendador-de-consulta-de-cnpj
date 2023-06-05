
from apps.extensions.db import db


class SQLAlchemyRepository:
    def commit(self):
        try:
            db.session.commit()
        except Exception as err:
            raise err

    def close(self):
        try:
            db.session.close()
        except Exception as err:
            raise err
