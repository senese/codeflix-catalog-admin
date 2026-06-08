from uuid import UUID

from src.core.cast_member.domain.cast_member import CastMember
from src.core.cast_member.domain.cast_member_repository import CastMemberRepository
from src.django_project.cast_member_app.models import CastMember as CastMemberORM


class DjangoORMCastMemberRepository(CastMemberRepository):
    def save(self, cast_member: CastMember) -> None:
        CastMemberORM.objects.create(
            id=cast_member.id,
            name=cast_member.name,
            type=cast_member.type,
        )

    def get_by_id(self, id: UUID) -> CastMember | None:
        try:
            cm = CastMemberORM.objects.get(id=id)
            return CastMember(
                id=cm.id,
                name=cm.name,
                type=CastMember.Type(cm.type),
            )
        except CastMemberORM.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        CastMemberORM.objects.filter(id=id).delete()

    def list(self) -> list[CastMember]:
        return [
            CastMember(
                id=cm.id,
                name=cm.name,
                type=CastMember.Type(cm.type),
            )
            for cm in CastMemberORM.objects.all()
        ]

    def update(self, cast_member: CastMember) -> None:
        CastMemberORM.objects.filter(pk=cast_member.id).update(
            name=cast_member.name,
            type=cast_member.type,
        )
