import pytest
from src import config
from src.core._shared.application.list_pagination import ListOutputMeta, ListRequest
from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
    ListCastMemberResponse,
)
from src.core.cast_member.domain.cast_member import CastMember, CastMemberType
from src.core.cast_member.infra.in_memory_cast_member_repository import (
    InMemoryCastMemberRepository,
)


class TestListCastMember:
    @pytest.fixture
    def actor(self) -> CastMember:
        return CastMember(
            name="John Doe",
            type=CastMemberType.ACTOR,
        )

    @pytest.fixture
    def actor2(self) -> CastMember:
        return CastMember(
            name="Jane Doe",
            type=CastMemberType.ACTOR,
        )

    @pytest.fixture
    def director(self) -> CastMember:
        return CastMember(
            name="John Krasinski",
            type=CastMemberType.DIRECTOR,
        )

    def test_when_no_cast_members_then_return_empty_list(self) -> None:
        empty_repository = InMemoryCastMemberRepository()
        use_case = ListCastMember(repository=empty_repository)
        response = use_case.execute(request=ListRequest())

        assert response == ListCastMemberResponse(
            data=[],
            meta=ListOutputMeta(
                current_page=1,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=0
            )
        )

    def test_when_cast_members_exist_then_return_mapped_list(
        self,
        actor: CastMember,
        director: CastMember,
    ) -> None:
        repository = InMemoryCastMemberRepository()
        repository.save(cast_member=actor)
        repository.save(cast_member=director)

        use_case = ListCastMember(repository=repository)
        response = use_case.execute(request=ListRequest())

        assert response == ListCastMemberResponse(
            data=[
                CastMemberOutput(
                    id=actor.id,
                    name=actor.name,
                    type=actor.type,
                ),
                CastMemberOutput(
                    id=director.id,
                    name=director.name,
                    type=director.type,
                ),
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=2
            )
        )

    def test_when_cast_members_have_multiple_pages(
        self,
        actor: CastMember,
        actor2: CastMember,
        director: CastMember,
    ) -> None:
        repository = InMemoryCastMemberRepository()
        repository.save(cast_member=actor)
        repository.save(cast_member=actor2)
        repository.save(cast_member=director)

        use_case = ListCastMember(repository=repository)
        response = use_case.execute(request=ListRequest())

        assert response == ListCastMemberResponse(
            data=[
                CastMemberOutput(
                    id=actor2.id,
                    name=actor2.name,
                    type=actor2.type,
                ),
                CastMemberOutput(
                    id=actor.id,
                    name=actor.name,
                    type=actor.type,
                )
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=3
            ),
        )

        response = use_case.execute(request=ListRequest(current_page=2))
        assert response == ListCastMemberResponse(
            data=[
                CastMemberOutput(
                    id=director.id,
                    name=director.name,
                    type=director.type,
                )
            ],
            meta=ListOutputMeta(
                current_page=2,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=3
            ),
        )
