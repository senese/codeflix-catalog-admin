import pytest

from src.core.cast_member.domain.cast_member import CastMember
from src.django_project.cast_member_app.models import CastMember as CastMemberORM
from src.django_project.cast_member_app.repository import DjangoORMCastMemberRepository


@pytest.mark.django_db
class TestSave:
    def test_saves_cast_member_in_database(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = DjangoORMCastMemberRepository()

        assert CastMemberORM.objects.count() == 0
        repository.save(cast_member)
        assert CastMemberORM.objects.count() == 1

        saved = CastMemberORM.objects.get()
        assert saved.id == cast_member.id
        assert saved.name == "John Doe"
        assert saved.type == "ACTOR"


@pytest.mark.django_db
class TestGetById:
    def test_returns_cast_member_when_found(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member)

        result = repository.get_by_id(cast_member.id)

        assert result == cast_member
        assert result.name == "John Doe"
        assert result.type == CastMember.Type.actor

    def test_returns_none_when_not_found(self):
        import uuid
        repository = DjangoORMCastMemberRepository()

        result = repository.get_by_id(uuid.uuid4())

        assert result is None


@pytest.mark.django_db
class TestDelete:
    def test_deletes_cast_member_from_database(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member)

        assert CastMemberORM.objects.count() == 1
        repository.delete(cast_member.id)
        assert CastMemberORM.objects.count() == 0


@pytest.mark.django_db
class TestUpdate:
    def test_updates_cast_member_in_database(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        repository = DjangoORMCastMemberRepository()
        repository.save(cast_member)

        cast_member.change_name("Jane Doe")
        cast_member.change_type(CastMember.Type.director)
        repository.update(cast_member)

        updated = CastMemberORM.objects.get(id=cast_member.id)
        assert updated.name == "Jane Doe"
        assert updated.type == "DIRECTOR"


@pytest.mark.django_db
class TestList:
    def test_returns_all_cast_members(self):
        actor = CastMember(name="John Doe", type=CastMember.Type.actor)
        director = CastMember(name="Jane Doe", type=CastMember.Type.director)
        repository = DjangoORMCastMemberRepository()
        repository.save(actor)
        repository.save(director)

        result = repository.list()

        assert len(result) == 2
