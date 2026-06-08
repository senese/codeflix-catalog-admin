import uuid
from uuid import UUID

import pytest

from src.core.cast_member.domain.cast_member import CastMember


class TestCastMember:
    def test_name_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'name'"):
            CastMember(type=CastMember.Type.actor)

    def test_type_is_required(self):
        with pytest.raises(TypeError, match="missing 1 required positional argument: 'type'"):
            CastMember(name="John Doe")

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            CastMember(name="a" * 256, type=CastMember.Type.actor)

    def test_cannot_create_cast_member_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember(name="", type=CastMember.Type.actor)

    def test_id_is_generated_as_uuid_by_default(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        assert isinstance(cast_member.id, UUID)

    def test_create_cast_member(self):
        member_id = uuid.uuid4()
        cast_member = CastMember(
            id=member_id,
            name="John Doe",
            type=CastMember.Type.director,
        )
        assert cast_member.id == member_id
        assert cast_member.name == "John Doe"
        assert cast_member.type == CastMember.Type.director

    def test_type_accepts_actor_and_director(self):
        actor = CastMember(name="John", type=CastMember.Type.actor)
        director = CastMember(name="Jane", type=CastMember.Type.director)
        assert actor.type == CastMember.Type.actor
        assert director.type == CastMember.Type.director

    def test_type_dont_accept_invalid_values(self):
        with pytest.raises(ValueError):
            CastMember(name="John", type="INVALID")


class TestCastMemberEquality:
    def test_cast_members_with_same_id_are_equal(self):
        member_id = uuid.uuid4()
        cm1 = CastMember(id=member_id, name="John", type=CastMember.Type.actor)
        cm2 = CastMember(id=member_id, name="Jane", type=CastMember.Type.director)
        assert cm1 == cm2

    def test_cast_members_with_different_ids_are_not_equal(self):
        cm1 = CastMember(name="John", type=CastMember.Type.actor)
        cm2 = CastMember(name="John", type=CastMember.Type.actor)
        assert cm1 != cm2


class TestChangeName:
    def test_change_name(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        cast_member.change_name("Jane Doe")
        assert cast_member.name == "Jane Doe"

    def test_change_name_to_invalid_raises_exception(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            cast_member.change_name("a" * 256)

    def test_change_name_to_empty_raises_exception(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        with pytest.raises(ValueError, match="name cannot be empty"):
            cast_member.change_name("")


class TestChangeType:
    def test_change_type_from_actor_to_director(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.actor)
        cast_member.change_type(CastMember.Type.director)
        assert cast_member.type == CastMember.Type.director

    def test_change_type_from_director_to_actor(self):
        cast_member = CastMember(name="John Doe", type=CastMember.Type.director)
        cast_member.change_type(CastMember.Type.actor)
        assert cast_member.type == CastMember.Type.actor
