from src.interfaces.rest_api.dependencies.logger import LoggerDep
from src.interfaces.rest_api.dependencies.use_cases import (
    GetAllTickerDataFilteredUseCaseDep,
    GetAllTickerDataUseCaseDep,
    GetTickerLastRecordUseCaseDep,
)

__all__ = [
    "LoggerDep",
    "GetAllTickerDataFilteredUseCaseDep",
    "GetAllTickerDataUseCaseDep",
    "GetTickerLastRecordUseCaseDep",
]
