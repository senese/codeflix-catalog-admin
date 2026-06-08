import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestCreateEditAndDeleteCastMember:
    def test_user_can_create_edit_and_delete_cast_member(self, api_client: APIClient) -> None:
        list_response = api_client.get("/api/cast_members/")
        assert list_response.status_code == 200
        assert list_response.data == {"data": []}

        create_response = api_client.post(
            "/api/cast_members/",
            {
                "name": "John Doe",
                "type": "ACTOR",
            },
        )
        assert create_response.status_code == 201
        created_cast_member_id = create_response.data["id"]

        assert api_client.get("/api/cast_members/").data == {
            "data": [
                {
                    "id": created_cast_member_id,
                    "name": "John Doe",
                    "type": "ACTOR",
                }
            ]
        }

        update_response = api_client.put(
            f"/api/cast_members/{created_cast_member_id}/",
            {
                "name": "Jane Doe",
                "type": "DIRECTOR",
            },
        )
        assert update_response.status_code == 204

        assert api_client.get("/api/cast_members/").data == {
            "data": [
                {
                    "id": created_cast_member_id,
                    "name": "Jane Doe",
                    "type": "DIRECTOR",
                }
            ]
        }

        delete_response = api_client.delete(f"/api/cast_members/{created_cast_member_id}/")
        assert delete_response.status_code == 204

        assert api_client.get("/api/cast_members/").data == {"data": []}
