from dataclasses import dataclass, field
from enum import StrEnum
import uuid


@dataclass
class CastMember:
    class Type(StrEnum):
        actor = "ACTOR"
        director = "DIRECTOR"

    name: str
    type: Type
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255")

        if not self.name:
            raise ValueError("name cannot be empty")

        if self.type not in CastMember.Type:
            raise ValueError(f"type must be one of {list(CastMember.Type)}")

    def __str__(self):
        return f"{self.name} (type: {self.type.value})"

    def __repr__(self):
        return f"<CastMember {self.name} ({self.type.value})>"

    def __eq__(self, other):
        if not isinstance(other, CastMember):
            return False

        return self.id == other.id

    def change_name(self, name):
        old_name = self.name
        self.name = name
        try:
            self.validate()
        except ValueError:
            self.name = old_name
            raise

    def change_type(self, type: "CastMember.Type"):
        old_type = self.type
        self.type = type
        try:
            self.validate()
        except ValueError:
            self.type = old_type
            raise
