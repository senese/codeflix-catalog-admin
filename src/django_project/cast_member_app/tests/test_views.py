from uuid import UUID, uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from src.core.cast_member.domain.cast_member import CastMember
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.fixture
def cast_member_actor() -> CastMember:
    return CastMember(
        name="John Doe",
        type=CastMember.Type.actor,
    )


@pytest.fixture
def cast_member_director() -> CastMember:
    return CastMember(
        name="Jane Doe",
        type=CastMember.Type.director,
    )


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:
    def test_list_cast_members(
        self,
        cast_member_actor: CastMember,
        cast_member_director: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        cast_member_repository.save(cast_member_actor)
        cast_member_repository.save(cast_member_director)

        response = APIClient().get("/api/cast_members/")

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data["data"][0]["id"] == str(cast_member_actor.id)
        assert response.data["data"][0]["name"] == "John Doe"
        assert response.data["data"][0]["type"] == "ACTOR"
        assert response.data["data"][1]["id"] == str(cast_member_director.id)
        assert response.data["data"][1]["name"] == "Jane Doe"
        assert response.data["data"][1]["type"] == "DIRECTOR"


@pytest.mark.django_db
class TestCreateAPI:
    def test_when_request_data_is_valid_then_create_cast_member(
        self,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        response = APIClient().post(
            "/api/cast_members/",
            data={
                "name": "John Doe",
                "type": "ACTOR",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["id"]

        saved = cast_member_repository.get_by_id(response.data["id"])
        assert saved == CastMember(
            id=UUID(response.data["id"]),
            name="John Doe",
            type=CastMember.Type.actor,
        )

    def test_when_request_data_is_invalid_then_return_400(self) -> None:
        response = APIClient().post(
            "/api/cast_members/",
            data={
                "name": "",
                "type": "ACTOR",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_type_is_invalid_then_return_400(self) -> None:
        response = APIClient().post(
            "/api/cast_members/",
            data={
                "name": "John Doe",
                "type": "INVALID",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "type" in response.data


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_cast_member(
        self,
        cast_member_actor: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        cast_member_repository.save(cast_member_actor)

        response = APIClient().put(
            f"/api/cast_members/{cast_member_actor.id}/",
            data={
                "name": "Jane Doe",
                "type": "DIRECTOR",
            },
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        updated = cast_member_repository.get_by_id(cast_member_actor.id)
        assert updated.name == "Jane Doe"
        assert updated.type == CastMember.Type.director

    def test_when_request_data_is_invalid_then_return_400(
        self,
        cast_member_actor: CastMember,
    ) -> None:
        response = APIClient().put(
            f"/api/cast_members/{cast_member_actor.id}/",
            data={
                "name": "",
                "type": "ACTOR",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_type_is_invalid_then_return_400(
        self,
        cast_member_actor: CastMember,
    ) -> None:
        response = APIClient().put(
            f"/api/cast_members/{cast_member_actor.id}/",
            data={
                "name": "John Doe",
                "type": "INVALID",
            },
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "type" in response.data

    def test_when_cast_member_does_not_exist_then_return_404(self) -> None:
        response = APIClient().put(
            f"/api/cast_members/{uuid4()}/",
            data={
                "name": "John Doe",
                "type": "ACTOR",
            },
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestDeleteAPI:
    def test_when_cast_member_pk_is_invalid_then_return_400(self) -> None:
        response = APIClient().delete("/api/cast_members/invalid_uuid/")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data == {"id": ["Must be a valid UUID."]}

    def test_when_cast_member_not_found_then_return_404(self) -> None:
        response = APIClient().delete(f"/api/cast_members/{uuid4()}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_when_cast_member_found_then_delete_cast_member(
        self,
        cast_member_actor: CastMember,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        cast_member_repository.save(cast_member_actor)

        response = APIClient().delete(f"/api/cast_members/{cast_member_actor.id}/")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert cast_member_repository.get_by_id(cast_member_actor.id) is None
