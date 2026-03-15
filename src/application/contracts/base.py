from pydantic import BaseModel


class Command(BaseModel):
    model_config = {"extra": "forbid"}

    def safe_dump(self) -> dict[str, object]:
        return self.model_dump()


class Result(BaseModel):
    model_config = {"extra": "forbid"}

    def safe_dump(self) -> dict[str, object]:
        return self.model_dump()


class NoneResult(Result):
    pass
