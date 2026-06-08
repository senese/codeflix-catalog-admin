from dataclasses import dataclass
from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: CastMember.Type


class ListCastMember:
    def __init__(self, repository: CastMemberRepository):
        self.repository = repository

    @dataclass
    class Input:
        pass

    @dataclass
    class Output:
        data: list[CastMemberOutput]

    def execute(self, input: Input) -> Output:
        cast_members = self.repository.list()

        return self.Output(
            data=[
                CastMemberOutput(
                    id=cm.id,
                    name=cm.name,
                    type=cm.type,
                )
                for cm in cast_members
            ]
        )
