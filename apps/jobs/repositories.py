from logging import Logger

from apps.extensions.db import db
from apps.jobs.models import Job

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


class JobsSQLAlchemyRepository(SQLAlchemyRepository):
    def __init__(self, logger: Logger | None = None) -> None:
        self.logger = logger

    def _get(self, job_id: str):
        return True

    def insert(self, data) -> None:
        try:
            job = Job(**data)
            db.session.add(job)
            self.commit()

            if self.logger:
                self.logger.info("create.job.sqlalchemy.repository", message="created")
            return job

        except Exception as err:
            raise err

    def get_jobs_paginated(self, page_id=1, page_size=10):
        try:
            if self.logger:
                self.logger.info("create.job.sqlalchemy.repository", message="fetch paginated")
            return 'foo'

        except Exception as err:
            raise err

    def get_job_by_id(self, job_id: str):
        try:
            if self.logger:
                self.logger.info("create.job.sqlalchemy.repository", message="get job by id")

            return self._get(job_id=job_id)

        except Exception as err:
            raise err

    def delete(self, job):
        try:
            founded = self._get(job_id=job.id)

            if self.logger:
                self.logger.info("create.job.sqlalchemy.repository", message="deleted job")

            return 'foo'

        except Exception as err:
            raise err

