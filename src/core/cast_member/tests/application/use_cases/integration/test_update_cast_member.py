import uuid

import pytest

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestUpdateCastMember:
    def test_update_cast_member_name_and_type(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        use_case = UpdateCastMember(repository=repository)
        use_case.execute(UpdateCastMember.Input(
            id=cast_member.id,
            name="Jane Doe",
            type=CastMember.Type.director,
        ))

        updated = repository.get_by_id(cast_member.id)
        assert updated.name == "Jane Doe"
        assert updated.type == CastMember.Type.director

    def test_when_cast_member_not_found_then_raise_not_found(self):
        repository = InMemoryCastMemberRepository()

        use_case = UpdateCastMember(repository=repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(UpdateCastMember.Input(
                id=uuid.uuid4(),
                name="John Doe",
                type=CastMember.Type.actor,
            ))

    def test_when_name_is_invalid_then_raise_invalid_and_do_not_update(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        use_case = UpdateCastMember(repository=repository)

        with pytest.raises(InvalidCastMember):
            use_case.execute(UpdateCastMember.Input(
                id=cast_member.id,
                name="",
                type=CastMember.Type.actor,
            ))

        unchanged = repository.get_by_id(cast_member.id)
        assert unchanged.name == "John Doe"

    def test_when_type_is_invalid_then_raise_invalid_and_do_not_update(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = InMemoryCastMemberRepository(cast_members=[cast_member])

        use_case = UpdateCastMember(repository=repository)

        with pytest.raises(InvalidCastMember):
            use_case.execute(UpdateCastMember.Input(
                id=cast_member.id,
                name="John Doe",
                type="INVALID",
            ))

        unchanged = repository.get_by_id(cast_member.id)
        assert unchanged.type == CastMember.Type.actor
