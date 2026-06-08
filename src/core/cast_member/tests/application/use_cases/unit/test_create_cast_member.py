from unittest.mock import create_autospec
from uuid import UUID

import pytest

from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        repository = create_autospec(CastMemberRepository)
        use_case = CreateCastMember(repository=repository)

        output = use_case.execute(CreateCastMember.Input(
            name="John Doe",
            type=CastMember.Type.actor,
        ))

        assert isinstance(output.id, UUID)
        repository.save.assert_called_once()

    def test_create_cast_member_as_director(self):
        repository = create_autospec(CastMemberRepository)
        use_case = CreateCastMember(repository=repository)

        output = use_case.execute(CreateCastMember.Input(
            name="Jane Doe",
            type=CastMember.Type.director,
        ))

        assert isinstance(output.id, UUID)
        repository.save.assert_called_once()

    def test_create_cast_member_with_empty_name_raises_invalid(self):
        repository = create_autospec(CastMemberRepository)
        use_case = CreateCastMember(repository=repository)

        with pytest.raises(InvalidCastMember, match="name cannot be empty"):
            use_case.execute(CreateCastMember.Input(name="", type=CastMember.Type.actor))

        repository.save.assert_not_called()

    def test_create_cast_member_with_long_name_raises_invalid(self):
        repository = create_autospec(CastMemberRepository)
        use_case = CreateCastMember(repository=repository)

        with pytest.raises(InvalidCastMember, match="name cannot be longer than 255"):
            use_case.execute(CreateCastMember.Input(name="a" * 256, type=CastMember.Type.actor))

        repository.save.assert_not_called()

    def test_create_cast_member_with_invalid_type_raises_invalid(self):
        repository = create_autospec(CastMemberRepository)
        use_case = CreateCastMember(repository=repository)

        with pytest.raises(InvalidCastMember):
            use_case.execute(CreateCastMember.Input(name="John Doe", type="INVALID"))

        repository.save.assert_not_called()
