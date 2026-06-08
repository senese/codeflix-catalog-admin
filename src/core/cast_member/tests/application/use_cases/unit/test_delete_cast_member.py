import uuid
from unittest.mock import create_autospec

import pytest

from src.core.cast_member.application.use_cases.delete_cast_member import DeleteCastMember
from src.core.cast_member.application.use_cases.exceptions import CastMemberNotFound
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestDeleteCastMember:
    def test_delete_cast_member(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = cast_member

        use_case = DeleteCastMember(repository=repository)
        use_case.execute(DeleteCastMember.Input(id=cast_member.id))

        repository.delete.assert_called_once_with(id=cast_member.id)

    def test_when_cast_member_not_found_then_raise_not_found(self):
        repository = create_autospec(CastMemberRepository)
        repository.get_by_id.return_value = None

        use_case = DeleteCastMember(repository=repository)

        with pytest.raises(CastMemberNotFound):
            use_case.execute(DeleteCastMember.Input(id=uuid.uuid4()))

        repository.delete.assert_not_called()
