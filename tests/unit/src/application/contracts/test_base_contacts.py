import pytest
from pydantic import ValidationError

from src.application.contracts.base import Command, NoneResult, Result


class TestCommand:
    def test_command_forbids_extra_fields(self):
        class TestCommand(Command):
            field1: str

        with pytest.raises(ValidationError):
            TestCommand.model_validate(
                {
                    "field1": "value",
                    "extra": "not allowed",
                }
            )

    def test_command_safe_dump(self):
        class TestCommand(Command):
            field1: str
            field2: int

        cmd = TestCommand(field1="test", field2=42)

        data = cmd.safe_dump()

        assert isinstance(data, dict)
        assert data["field1"] == "test"
        assert data["field2"] == 42

    def test_command_can_override_safe_dump(self):
        class TestCommand(Command):
            public_field: str
            sensitive_field: str

            def safe_dump(self) -> dict[str, object]:
                return self.model_dump(exclude={"sensitive_field"})

        cmd = TestCommand(
            public_field="public",
            sensitive_field="secret",
        )

        safe_data = cmd.safe_dump()

        assert "public_field" in safe_data
        assert "sensitive_field" not in safe_data


class TestResult:
    def test_result_forbids_extra_fields(self):
        class TestResult(Result):
            value: int

        with pytest.raises(ValidationError):
            TestResult.model_validate(
                {
                    "value": 42,
                    "extra": "not allowed",
                }
            )

    def test_result_safe_dump(self):
        class TestResult(Result):
            success: bool
            message: str

        result = TestResult(success=True, message="Operation successful")

        data = result.safe_dump()

        assert isinstance(data, dict)
        assert data["success"] is True
        assert data["message"] == "Operation successful"

    def test_result_can_override_safe_dump(self):
        class TestResult(Result):
            success: bool
            sensitive_result_data: str

            def safe_dump(self) -> dict[str, object]:
                return self.model_dump(exclude={"sensitive_result_data"})

        result = TestResult(
            success=True,
            sensitive_result_data="secret",
        )

        safe_data = result.safe_dump()

        assert "success" in safe_data
        assert "sensitive_result_data" not in safe_data


class TestNoneResult:
    def test_create_none_result(self):
        result = NoneResult()

        assert isinstance(result, Result)

    def test_none_result_forbids_extra_fields(self):
        with pytest.raises(ValidationError):
            NoneResult.model_validate({"extra_field": "not allowed"})

    def test_none_result_safe_dump(self):
        result = NoneResult()
        safe_data = result.safe_dump()

        assert isinstance(safe_data, dict)
        assert len(safe_data) == 0
