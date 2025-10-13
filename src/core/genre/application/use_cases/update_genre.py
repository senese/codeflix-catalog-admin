from dataclasses import dataclass, field
from uuid import UUID

from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


class UpdateGenre:
    def __init__(self, repository: GenreRepository, category_repository: CategoryRepository):
        self.repository = repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        id: UUID
        name: str | None
        is_active: bool | None
        categories: set[UUID] | None

    @dataclass
    class Output:
        id: UUID
        name: str
        is_active: bool
        categories: set[UUID]

    def execute(self, input: Input) -> Output:
        genre = self.repository.get_by_id(input.id)
        if not genre:
            raise GenreNotFound(f"Genre with provided ID not found: {input.id}")

        category_ids = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {input.categories - category_ids}")

        try:
            genre = Genre(
                id=input.id,
                name=input.name,
                is_active=input.is_active,
                categories=category_ids,
            )
        except ValueError as err:
            raise InvalidGenre(err)

        self.repository.update(genre)
        return self.Output(
            id=genre.id,
            name=input.name,
            is_active=input.is_active,
            categories=input.categories
        )
