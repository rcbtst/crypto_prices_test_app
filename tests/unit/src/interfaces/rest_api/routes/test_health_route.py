import pytest


class TestHealthRoute:
    @pytest.mark.asyncio
    async def test_health_check_success(self, test_rest_api_client):
        response = await test_rest_api_client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["health"] == "OK"
