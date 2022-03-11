import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class FilmworkMixin(models.Model):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('genre')
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Filmwork(UUIDMixin, TimeStampedMixin):
    class Type(models.TextChoices):
        MOVIE = 'movie', _('film')
        TV_SHOW = 'tv_show', _('TV show')

    title = models.CharField(_('title'), max_length=255)
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'), blank=True)
    rating = models.DecimalField(_('rating'), max_digits=2, decimal_places=1, blank=True,
                                 validators=[MinValueValidator(0), MaxValueValidator(10)])
    category = models.CharField(_('type'), max_length=20, choices=Type.choices, default=Type.MOVIE,
                                db_column='type')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('film_work')
        verbose_name_plural = 'Кинопроизведения'

    def __str__(self):
        return self.title


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('person')
        verbose_name_plural = 'Актер'

    def __str__(self):
        return self.full_name


class GenreFilmwork(UUIDMixin, FilmworkMixin):
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"genre_film_work"


class PersonFilmwork(UUIDMixin, FilmworkMixin):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), blank=True, max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "content\".\"person_film_work"
