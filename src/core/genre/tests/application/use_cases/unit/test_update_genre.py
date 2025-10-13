from uuid import uuid4
from unittest.mock import create_autospec

import pytest

from src.core.category.domain.category import Category
from src.core.category.domain.category_repository import CategoryRepository
from src.core.genre.application.use_cases.exceptions import GenreNotFound, InvalidGenre, RelatedCategoriesNotFound
from src.core.genre.application.use_cases.update_genre import UpdateGenre
from src.core.genre.domain.genre import Genre
from src.core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mock_genre(movie_category) -> Genre:
    return Genre(name="Comedy", is_active=True, categories={movie_category.id})


@pytest.fixture
def mock_genre_repository(mock_genre) -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.get_by_id.return_value = mock_genre
    return repository


@pytest.fixture
def mock_empty_genre_repository() -> GenreRepository:
    repository = create_autospec(GenreRepository)
    repository.get_by_id.return_value = None
    return repository


@pytest.fixture
def mock_category_repository_with_categories(movie_category, documentary_category) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


class TestUpdateGenre:
    def test_when_updated_inexistent_genre_then_raise_genre_not_found(
        self,
        mock_category_repository_with_categories,
        mock_empty_genre_repository,
    ) -> None:
        use_case = UpdateGenre(
            repository=mock_empty_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )

        with pytest.raises(GenreNotFound, match="Genre with provided ID not found:"):
            use_case.execute(UpdateGenre.Input(
                id=uuid4(),
                name="Drama",
                is_active=True,
                categories={uuid4()},
            ))

    def test_when_updated_genre_is_invalid_then_raise_invalid_genre(
        self,
        mock_genre,
        movie_category,
        mock_category_repository_with_categories,
        mock_genre_repository,
    ) -> None:
        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )

        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            use_case.execute(UpdateGenre.Input(
                id=mock_genre.id,
                name="",
                is_active=True,
                categories={movie_category.id},
            ))

    def test_when_provided_categories_do_not_exist_then_raise_related_categories_not_found(
        self,
        mock_genre,
        mock_genre_repository,
        mock_empty_category_repository,
    ):
        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_empty_category_repository,
        )

        with pytest.raises(RelatedCategoriesNotFound, match="Categories with provided IDs not found: ") as exc:
            category_id = uuid4()
            use_case.execute(UpdateGenre.Input(
                id=mock_genre.id,
                name="Genre 1",
                is_active=True,
                categories={category_id},
            ))

        assert str(category_id) in str(exc.value)

    def test_update_genre_with_new_name_and_not_active(
        self,
        movie_category,
        mock_genre,
        mock_genre_repository,
        mock_category_repository_with_categories,
    ):
        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )

        input = UpdateGenre.Input(
            id=mock_genre.id,
            name="Romance",
            is_active=False,
            categories={movie_category.id},
        )
        output = use_case.execute(input)

        mock_genre_repository.update.assert_called_once_with(
            Genre(
                id=mock_genre.id,
                name="Romance",
                is_active=False,
                categories={movie_category.id},
            )
        )
        assert output == UpdateGenre.Output(
            id=mock_genre.id,
            name=input.name,
            is_active=input.is_active,
            categories=input.categories
        )

    def test_update_genre_with_new_categories(
        self,
        movie_category,
        documentary_category,
        mock_genre,
        mock_genre_repository,
        mock_category_repository_with_categories,
    ):
        use_case = UpdateGenre(
            repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )

        input = UpdateGenre.Input(
            id=mock_genre.id,
            name="Comedy",
            is_active=True,
            categories={documentary_category.id, movie_category.id},
        )
        output = use_case.execute(input)

        mock_genre_repository.update.assert_called_once_with(
            Genre(
                id=mock_genre.id,
                name="Comedy",
                is_active=True,
                categories={documentary_category.id, movie_category.id},
            )
        )
        assert output == UpdateGenre.Output(
            id=mock_genre.id,
            name=input.name,
            is_active=input.is_active,
            categories=input.categories
        )
