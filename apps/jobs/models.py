from enum import StrEnum
from apps.extensions.db import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from apps.results.models import Result
class JobStatusEnum(StrEnum):
    created = 'created'
    processed = 'processed'
    error = 'error'
    processing = 'processing'


class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text, nullable=False)
    cpf_cnpj = db.Column(db.String(), nullable=False)
    status = db.Column(db.Enum(JobStatusEnum), default=JobStatusEnum.created)
    # low priority with rabbitmq
    priority = db.Column(db.Integer, default=0)
    duration = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    creator_id = db.Column(db.String(), nullable=False)
    creator_email = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    results = db.relationship(Result, back_populates="job")

    def to_dict(self):
        return self._asdict()
        # return {field.name:getattr(self, field.name) for field in self.__table__.c}
