import uuid
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.application.use_cases.update_cast_member import UpdateCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestUpdateCastMember:
    def test_update_cast_member_name(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=repository)
        use_case.execute(UpdateCastMember.Input(
            id=cast_member.id,
            name="Jane Doe",
            type=CastMember.Type.actor,
        ))

        assert cast_member.name == "Jane Doe"
        repository.update.assert_called_once_with(cast_member)

    def test_update_cast_member_type(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=repository)
        use_case.execute(UpdateCastMember.Input(
            id=cast_member.id,
            name="John Doe",
            type=CastMember.Type.director,
        ))

        assert cast_member.type == CastMember.Type.director
        repository.update.assert_called_once_with(cast_member)

    def test_update_cast_member_name_and_type(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=repository)
        use_case.execute(UpdateCastMember.Input(
            id=cast_member.id,
            name="Jane Doe",
            type=CastMember.Type.director,
        ))

        assert cast_member.name == "Jane Doe"
        assert cast_member.type == CastMember.Type.director
        repository.update.assert_called_once_with(cast_member)

    def test_when_cast_member_not_found_then_raise_not_found(self):
        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = None

        use_case = UpdateCastMember(repository=repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(UpdateCastMember.Input(
                id=uuid.uuid4(),
                name="John Doe",
                type=CastMember.Type.actor,
            ))

        repository.update.assert_not_called()

    def test_when_name_is_invalid_then_raise_invalid(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=repository)

        with pytest.raises(InvalidCastMember):
            use_case.execute(UpdateCastMember.Input(
                id=cast_member.id,
                name="",
                type=CastMember.Type.actor,
            ))

        repository.update.assert_not_called()

    def test_when_type_is_invalid_then_raise_invalid(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = cast_member

        use_case = UpdateCastMember(repository=repository)

        with pytest.raises(InvalidCastMember):
            use_case.execute(UpdateCastMember.Input(
                id=cast_member.id,
                name="John Doe",
                type="INVALID",
            ))

        repository.update.assert_not_called()
