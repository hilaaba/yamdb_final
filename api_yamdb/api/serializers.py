import datetime as dt

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.models import Category, Comment, Genre, Review, Title
from users.validators import validate_user

User = get_user_model()


class GetConfirmationCodeSerializer(serializers.ModelSerializer):
    """
    Проверка username и email перед выдачей confirmation_code.
    """
    username = serializers.CharField(
        max_length=150,
        validators=[validate_user],
    )
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, data):
        if User.objects.filter(
            username=data['username']
        ).exclude(email=data['email']).exists():
            raise ValidationError(
                'Пользователь с таким username уже существует!'
            )
        if User.objects.filter(
            email=data['email']
        ).exclude(username=data['username']).exists():
            raise ValidationError('Пользователь с таким email уже существует!')
        return data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(**validated_data)
        return user


class GetTokenSerializer(serializers.Serializer):
    """
    Проверка username и confirmation_code перед выдачей токена.
    """
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    """
    Преобразует данные модели User для админов.
    """
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserMeSerializer(serializers.ModelSerializer):
    """
    Преобразует данные модели User при обращении от себя.
    """
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class GenresSerializer(serializers.ModelSerializer):
    """Жанры."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):
    """Категории."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitlesCreateSerializer(serializers.ModelSerializer):
    """Метод записи информации."""

    category = serializers.SlugRelatedField(
        slug_field='slug', many=False, queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте год')
        return value


class TitlesViewSerializer(serializers.ModelSerializer):
    """Метод получения информации."""

    category = CategoriesSerializer(many=False, required=True)
    genre = GenresSerializer(many=True, required=False)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    """Отзывы."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST' and Review.objects.filter(
            author=request.user,
            title=request.parser_context['kwargs'].get('title_id')
        ).exists():
            raise serializers.ValidationError(
                'Нельзя оставить больше одного отзыва на одно произведение'
            )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    """Комментарии."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author',)
