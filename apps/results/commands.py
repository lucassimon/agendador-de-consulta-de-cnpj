
from typing import Any, Mapping


from apps.extensions.logging import make_logger

from .repositories import ResultsSQLAlchemyRepository
from .schemas import ResultSchema
from .use_case import GetAllResultsByUserUseCase


logger = make_logger(debug=True)


class GetAllResultsCommand:
    @staticmethod
    def call_use_case(*_, **kwargs: dict[str, Any]):
        try:
            if logger:
                logger.info("get_all_results.job.command", message="Get all results")

            repo: ResultsSQLAlchemyRepository = ResultsSQLAlchemyRepository(logger=logger)

            use_case: GetAllResultsByUserUseCase = GetAllResultsByUserUseCase(
                repo=repo, logger=logger
            )

            if logger:
                logger.info("get_all_results.job.command", message="Execute use case")

            output: ResultSchema = use_case.execute(**kwargs)
            return output
        except Exception as exc:
            raise exc

    @staticmethod
    def run(*args, **kwargs: dict[str, Any]):
        output = GetAllResultsCommand.call_use_case(*args, **kwargs)

        return output

