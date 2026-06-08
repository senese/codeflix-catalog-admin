from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.application.use_cases.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)
from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class UpdateCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID
        name: str
        type: CastMember.Type

    def execute(self, input: Input) -> None:
        cast_member = self.repository.get_by_id(input.id)

        if cast_member is None:
            raise CastMemberNotFound(f"CastMember with id {input.id} not found")

        try:
            cast_member.change_name(input.name)
            cast_member.change_type(input.type)
        except ValueError as err:
            raise InvalidCastMember(err)

        self.repository.update(cast_member)
