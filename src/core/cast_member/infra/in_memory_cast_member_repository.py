from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, cast_members: list[CastMember] = None):
        self.cast_members: list[CastMember] = cast_members or []

    def save(self, cast_member: CastMember) -> None:
        self.cast_members.append(cast_member)

    def get_by_id(self, id: UUID) -> CastMember | None:
        return next(
            (cm for cm in self.cast_members if cm.id == id), None
        )

    def delete(self, id: UUID) -> None:
        cast_member = self.get_by_id(id)
        if cast_member:
            self.cast_members.remove(cast_member)

    def list(self) -> list[CastMember]:
        return list(self.cast_members)

    def update(self, cast_member: CastMember) -> None:
        old = self.get_by_id(cast_member.id)
        if old:
            self.cast_members.remove(old)
            self.cast_members.append(cast_member)
