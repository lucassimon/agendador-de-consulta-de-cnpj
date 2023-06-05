from logging import Logger
from flask import current_app

from marshmallow import ValidationError

from .repositories import ResultsSQLAlchemyRepository
from .schemas import ResultSchema


class GetAllResultsByUserUseCase:
    """
    Classe para buscar os results por usuário
    """

    def __init__(self, repo: ResultsSQLAlchemyRepository, logger: Logger | None = None) -> None:
        self.repo = repo
        self.logger = logger

    def __to_output(self, results):
        # Realizo um dump dos dados de acordo com o modelo salvo
        schema = ResultSchema(many=True)
        result = schema.dump(results)

        if self.logger:
            self.logger.info("get_all_results.job.usecase", message="Render job output")

        return result

    def fetch(self, *_, **kwargs):
        try:
            creator = kwargs['creator_id']
            job_id = kwargs['job_id']

            results = self.repo.get_all_results_user(
                creator_id=creator, job_id=job_id
            )

            if self.logger:
                self.logger.info("get_all_results.job.usecase", message="Results fetched")

            return results

        except Exception as err:
            if self.logger:
                self.logger.info("get_all_results.job.usecase", message="Resuls not fetched. Strange error")

            raise err

    def execute(self, **kwargs):
        results = self.fetch(**kwargs)
        output = self.__to_output(results=results)
        self.repo.close()
        return output
