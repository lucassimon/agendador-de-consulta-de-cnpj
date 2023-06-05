
from typing import Any, Mapping


from apps.extensions.logging import make_logger

from .repositories import JobsSQLAlchemyRepository
from .schemas import CreateJobInput, CreateJobOutput, PaginationJobsOutput
from .use_case import CreateJobUseCase, GetJobsPaginatedUseCase, GetJobUseCase


logger = make_logger(debug=True)


class CreateJobCommand:

    @staticmethod
    def call_use_case(payload: Mapping[str, Any], *_, **kwargs: dict[str, Any]):
        try:
            if logger:
                logger.info("create.job.command", message="Save in database operation")

            repo: JobsSQLAlchemyRepository = JobsSQLAlchemyRepository(logger=logger)
            schema = CreateJobInput()

            use_case: CreateJobUseCase = CreateJobUseCase(
                repo=repo, use_queue=kwargs['use_queue'], logger=logger
            )

            if logger:
                logger.info("create.job.command", message="Execute use case")

            output: CreateJobOutput = use_case.execute(schema_input=schema, input_params=payload, kwargs=kwargs)
            return output

        except Exception as exc:
            raise exc

    @staticmethod
    def run(payload: Mapping[str, Any], *args, **kwargs: dict[str, Any]):
        output = CreateJobCommand.call_use_case(payload, *args, **kwargs)

        return output


class GetJobsPaginatedCommand:
    @staticmethod
    def call_use_case(*_, **kwargs: dict[str, Any]):
        try:
            if logger:
                logger.info("get_jobs_paginated.job.command", message="Get jobs paginated")

            repo: JobsSQLAlchemyRepository = JobsSQLAlchemyRepository(logger=logger)

            use_case: GetJobsPaginatedUseCase = GetJobsPaginatedUseCase(
                repo=repo, logger=logger
            )

            if logger:
                logger.info("get_jobs_paginated.job.command", message="Execute use case")

            output: PaginationJobsOutput = use_case.execute(**kwargs)
            return output
        except Exception as exc:
            raise exc

    @staticmethod
    def run(*args, **kwargs: dict[str, Any]):
        output = GetJobsPaginatedCommand.call_use_case(*args, **kwargs)

        return output


class GetJobCommand:
    @staticmethod
    def call_use_case(*_, **kwargs: dict[str, Any]):
        try:
            if logger:
                logger.info("get_job.job.command", message="Fetch job")

            repo: JobsSQLAlchemyRepository = JobsSQLAlchemyRepository(logger=logger)

            use_case: GetJobUseCase = GetJobUseCase(repo=repo, logger=logger)

            if logger:
                logger.info("get_job.job.command", message="Execute use case")

            output: PaginationJobsOutput = use_case.execute(**kwargs)
            return output

        except Exception as exc:
            raise exc

    @staticmethod
    def run(*args, **kwargs: dict[str, Any]):
        output = GetJobCommand.call_use_case(*args, **kwargs)

        return output
