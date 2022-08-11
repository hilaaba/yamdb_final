import csv
import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()


def users_create(row):
    User.objects.get_or_create(
        id=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6],
    )


def category_create(row):
    Category.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def genre_create(row):
    Genre.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def titles_create(row):
    Title.objects.get_or_create(
        id=row[0],
        name=row[1],
        year=row[2],
        category_id=row[3],
    )


def genre_title_create(row):
    GenreTitle.objects.get_or_create(
        id=row[0],
        title_id=row[1],
        genre_id=row[2],
    )


def review_create(row):
    Review.objects.get_or_create(
        id=row[0],
        title_id=row[1],
        text=row[2],
        author_id=row[3],
        score=row[4],
        pub_date=row[5]
    )


def comment_create(row):
    Comment.objects.get_or_create(
        id=row[0],
        review_id=row[1],
        text=row[2],
        author_id=row[3],
        pub_date=row[4],
    )


filename_func_names = {
    'users.csv': users_create,
    'category.csv': category_create,
    'genre.csv': genre_create,
    'titles.csv': titles_create,
    'genre_title.csv': genre_title_create,
    'review.csv': review_create,
    'comments.csv': comment_create,
}


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for filename, func in filename_func_names.items():
            path = os.path.join(settings.BASE_DIR, "static/data/") + filename
            with open(path, 'r', encoding='utf-8') as file:
                data = csv.reader(file)
                next(data)
                for row in data:
                    func(row)
                print(f'Added {filename}')
