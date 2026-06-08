from src.core.cast_member.application.use_cases.list_cast_member import (
    CastMemberOutput,
    ListCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestListCastMember:
    def test_when_no_cast_members_then_return_empty_list(self):
        repository = InMemoryCastMemberRepository()

        use_case = ListCastMember(repository=repository)
        output = use_case.execute(ListCastMember.Input())

        assert output == ListCastMember.Output(data=[])

    def test_when_cast_members_exist_then_return_mapped_list(self):
        actor = CastMember(name="John Doe", type=CastMember.Type.actor)
        director = CastMember(name="Jane Doe", type=CastMember.Type.director)
        repository = InMemoryCastMemberRepository(cast_members=[actor, director])

        use_case = ListCastMember(repository=repository)
        output = use_case.execute(ListCastMember.Input())

        assert output == ListCastMember.Output(
            data=[
                CastMemberOutput(id=actor.id, name="John Doe", type=CastMember.Type.actor),
                CastMemberOutput(id=director.id, name="Jane Doe", type=CastMember.Type.director),
            ]
        )
