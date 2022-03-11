import uuid
from dataclasses import dataclass
from datetime import datetime

from dateutil import parser

from utils import cast_types, multiple_uuid_parse


@dataclass
class Filmwork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime
    rating: float
    type: str
    created: datetime
    modified: datetime

    def __post_init__(self):
        self.id, self.created, self.modified = cast_types(self.id, self.created, self.modified)
        if self.rating and not isinstance(self.rating, float):
            self.rating = float(self.rating)
        if isinstance(self.creation_date, str):
            self.creation_date = parser.parse(self.creation_date)

    def __eq__(self, other):
        return all(
            [
                self.id == other.id,
                self.title == other.title,
                self.description == other.description,
                self.creation_date == other.creation_date,
                self.rating == other.rating,
                self.type == other.type,
                self.created == other.created,
                self.modified == other.modified
            ]
        )


@dataclass
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created: datetime
    modified: datetime

    def __post_init__(self):
        self.id, self.created, self.modified = cast_types(self.id, self.created, self.modified)

    def __eq__(self, other):
        return all(
            [
                self.id == other.id,
                self.name == other.name,
                self.description == other.description,
                self.created == other.created,
                self.modified == other.modified
            ]
        )


@dataclass
class Person:
    id: uuid.UUID
    full_name: str
    created: datetime
    modified: datetime

    def __post_init__(self):
        self.id, self.created, self.modified = cast_types(self.id, self.created, self.modified)

    def __eq__(self, other):
        return all(
            [
                self.id == other.id,
                self.full_name == other.full_name,
                self.created == other.created,
                self.modified == other.modified
            ]
        )


@dataclass
class GenreFilmwork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created: datetime

    def __post_init__(self):
        self.id, self.film_work_id, self.genre_id = multiple_uuid_parse(self.id, self.film_work_id, self.genre_id)
        if isinstance(self.created, str):
            self.created = parser.parse(self.created)

    def __eq__(self, other):
        return all(
            [
                self.id == other.id,
                self.film_work_id == other.film_work_id,
                self.genre_id == other.genre_id,
                self.created == other.created
            ]
        )


@dataclass
class PersonFilmwork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created: datetime

    def __post_init__(self):
        self.id, self.film_work_id, self.person_id = multiple_uuid_parse(self.id, self.film_work_id, self.person_id)
        if isinstance(self.created, str):
            self.created = parser.parse(self.created)

    def __eq__(self, other):
        return all(
            [
                self.id == other.id,
                self.film_work_id == other.film_work_id,
                self.person_id == other.person_id,
                self.role == other.role,
                self.created == other.created
            ]
        )
