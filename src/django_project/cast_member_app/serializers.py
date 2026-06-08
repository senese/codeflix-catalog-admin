from rest_framework import serializers

from src.core.cast_member.domain.cast_member import CastMember


class CastMemberTypeField(serializers.ChoiceField):
    def __init__(self, **kwargs):
        choices = [(cast_member_type.value, cast_member_type.value) for cast_member_type in CastMember.Type]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return CastMember.Type(super().to_internal_value(data))

    def to_representation(self, value):
        if isinstance(value, CastMember.Type):
            return value.value

        return CastMember.Type(value).value


class CastMemberOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()


class ListCastMemberOutputSerializer(serializers.Serializer):
    data = CastMemberOutputSerializer(many=True)


class CreateCastMemberInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    type = CastMemberTypeField()


class CreateCastMemberOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class DeleteCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()


class UpdateCastMemberInputSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    name = serializers.CharField(required=True)
    type = CastMemberTypeField(required=True)
