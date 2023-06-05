from logging import Logger

from apps.extensions.db import db
from apps.results.models import Result
from apps.core.repositories import SQLAlchemyRepository


class ResultsSQLAlchemyRepository(SQLAlchemyRepository):
    def __init__(self, logger: Logger | None = None) -> None:
        self.logger = logger

    def get_all_results_user(self, creator_id, job_id):
        try:
            if self.logger:
                self.logger.info("get_all_results_user.results.sqlalchemy.repository", message="fetch all")

            pagination = Result.query.order_by(Result.created) \
                .filter(Result.creator_id==creator_id, Result.job_id==job_id).all()

            return pagination

        except Exception as err:
            raise err
