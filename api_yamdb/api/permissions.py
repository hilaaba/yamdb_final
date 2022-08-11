from rest_framework.permissions import SAFE_METHODS, BasePermission


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAuthorOrAdminPermission(BasePermission):
    """
    Доступ на изменение и удаление отзыва или комментария для авторов,
    админов или модераторов. Создание - для аутентифицированных пользователей.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )
