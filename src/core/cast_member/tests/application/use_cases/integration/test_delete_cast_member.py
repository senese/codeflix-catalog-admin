import uuid

import pytest

from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestDeleteCastMember:
    def test_delete_cast_member(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        use_case = DeleteCastMember(repository=repository)

        assert repository.get_by_id(cast_member.id) is not None
        use_case.execute(DeleteCastMember.Input(id=cast_member.id))
        assert repository.get_by_id(cast_member.id) is None

    def test_delete_only_the_specified_cast_member(self):
        actor = CastMember(name="John Doe", type=CastMember.Type.actor)
        director = CastMember(name="Jane Doe", type=CastMember.Type.director)
        repository = InMemoryCastMemberRepository(cast_members=[actor, director])

        use_case = DeleteCastMember(repository=repository)
        use_case.execute(DeleteCastMember.Input(id=actor.id))

        assert repository.get_by_id(actor.id) is None
        assert repository.get_by_id(director.id) == director

    def test_when_cast_member_not_found_then_raise_not_found(self):
        repository = InMemoryCastMemberRepository()

        use_case = DeleteCastMember(repository=repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(DeleteCastMember.Input(id=uuid.uuid4()))

        assert len(repository.cast_members) == 0
