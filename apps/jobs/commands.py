
from typing import Any, Mapping


from apps.extensions.logging import make_logger

from .repositories import JobsSQLAlchemyRepository
from .schemas import CreateJobInput, CreateJobOutput
from .use_case import CreateJobUseCase


logger = make_logger(debug=True)


class CreateJobCommand:

    @staticmethod
    def call_use_case(payload: Mapping[str, Any], *_, **kwargs: dict[str, Any]):
        try:
            if logger:
                logger.info("create.job.command", message="Save in database operation")

            repo: JobsSQLAlchemyRepository = JobsSQLAlchemyRepository(logger=logger)
            schema = CreateJobInput()
            import ipdb
            ipdb.set_trace()
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
