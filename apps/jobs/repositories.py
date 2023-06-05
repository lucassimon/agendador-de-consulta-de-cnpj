from logging import Logger

from apps.extensions.db import db
from apps.jobs.models import Job
from apps.core.repositories import SQLAlchemyRepository


class JobsSQLAlchemyRepository(SQLAlchemyRepository):
    def __init__(self, logger: Logger | None = None) -> None:
        self.logger = logger

    def _get(self, job_id: str, creator_id: str):
        job = Job.query.filter(Job.id == job_id, Job.creator_id==creator_id).one()

        return job

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

    def get_jobs_paginated_by_user(self, creator_id, page_id=1, page_size=10):
        try:
            if self.logger:
                self.logger.info("get_jobs_paginated_by_user.job.sqlalchemy.repository", message="fetch paginated")

            pagination = Job.query.order_by(Job.created) \
                .filter(Job.creator_id==creator_id) \
                .paginate(page=page_id, per_page=page_size)

            return pagination

        except Exception as err:
            raise err

    def get_job_by_id(self, job_id: str, creator_id: str):
        try:
            if self.logger:
                self.logger.info("get_job_by_id.job.sqlalchemy.repository", message="get job by id")

            return self._get(job_id=job_id, creator_id=creator_id)

        except Exception as err:
            raise err

    def delete(self, job):
        try:
            founded = self._get(job_id=job.id)

            if self.logger:
                self.logger.info("delete.job.sqlalchemy.repository", message="deleted job")

            return 'foo'

        except Exception as err:
            raise err

