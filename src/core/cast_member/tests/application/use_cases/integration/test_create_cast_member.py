import pytest

from src.core.cast_member.application.use_cases.create_cast_member import CreateCastMember
from src.core.cast_member.application.use_cases.exceptions import InvalidCastMember
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.infra.in_memory_cast_member_repository import InMemoryCastMemberRepository


class TestCreateCastMember:
    def test_create_cast_member_with_valid_data(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)

        output = use_case.execute(CreateCastMember.Input(
            name="John Doe",
            type=CastMember.Type.actor,
        ))

        assert output.id is not None
        assert len(repository.cast_members) == 1
        saved = repository.get_by_id(output.id)
        assert saved.name == "John Doe"
        assert saved.type == CastMember.Type.actor

    def test_create_cast_member_as_director(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)

        output = use_case.execute(CreateCastMember.Input(
            name="Jane Doe",
            type=CastMember.Type.director,
        ))

        saved = repository.get_by_id(output.id)
        assert saved.type == CastMember.Type.director

    def test_create_cast_member_with_empty_name_raises_invalid(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)

        with pytest.raises(InvalidCastMember, match="name cannot be empty"):
            use_case.execute(CreateCastMember.Input(name="", type=CastMember.Type.actor))

        assert len(repository.cast_members) == 0

    def test_create_cast_member_with_long_name_raises_invalid(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)

        with pytest.raises(InvalidCastMember, match="name cannot be longer than 255"):
            use_case.execute(CreateCastMember.Input(name="a" * 256, type=CastMember.Type.actor))

        assert len(repository.cast_members) == 0

    def test_create_cast_member_with_invalid_type_raises_invalid(self):
        repository = InMemoryCastMemberRepository()
        use_case = CreateCastMember(repository=repository)

        with pytest.raises(InvalidCastMember):
            use_case.execute(CreateCastMember.Input(name="John Doe", type="INVALID"))

        assert len(repository.cast_members) == 0
