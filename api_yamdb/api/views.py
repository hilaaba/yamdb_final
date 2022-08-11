from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.filters import TitleFilter
from reviews.models import Category, Genre, Review, Title

from .permissions import (AdminPermission, IsAdminOrReadOnly,
                          IsAuthorOrAdminPermission)
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, GetConfirmationCodeSerializer,
                          GetTokenSerializer, ReviewSerializer,
                          TitlesCreateSerializer, TitlesViewSerializer,
                          UserMeSerializer, UserSerializer)

User = get_user_model()


class GetConfirmationCodeView(APIView):
    """
    При POST-запросе с параметрами username и email отправляет
    confirmation_code на указанный email.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetConfirmationCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            email = serializer.validated_data['email']
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                subject='Ваш код подтверждения на сайте Yambd',
                message=f'Ваш код: {confirmation_code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenView(APIView):
    """
    При POST-запросе с параметрами username и confirmation_code возвращает
    JWT-токен.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = serializer.validated_data.get(
                'confirmation_code',
            )
            if default_token_generator.check_token(user, confirmation_code):
                access_token = RefreshToken.for_user(user).access_token
                return Response(
                    {'token': str(access_token)},
                    status=status.HTTP_201_CREATED,
                )
        return Response(
            {'error': 'Неправильный код подтверждения.'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    Выполняет следующие действия с моделью пользователей:
        Администратор:
            1. Получение списка всех пользователей.
            2. Добавление пользователя.
            3. Получение пользователя по username.
            4. Изменение данных пользователя по username.
            5. Удаление пользователя по username.
        Любой авторизованный пользователь:
            1. Получение данных своей учетной записи.
            2. Изменение данных своей учетной записи.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (AdminPermission,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('role', 'is_superuser')
    search_fields = ('username', 'email', 'role', 'bio')

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_patch_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserMeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserMeSerializer(
            user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitlesCreateSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesViewSerializer
        return TitlesCreateSerializer


class GenreModelMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CategoriesViewSet(GenreModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer


class GenresViewSet(GenreModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminPermission,
    )

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsAuthorOrAdminPermission,
    )

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id'),
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id'),
        )
        serializer.save(author=self.request.user, review=review)
