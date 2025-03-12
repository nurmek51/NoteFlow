from rest_framework import permissions


class isOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение: только владелец может редактировать или удалять материал,
    остальные могут только читать.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем чтение всем пользователям
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешаем изменение и удаление только владельцу материала
        return obj.uploaded_by == request.user

class isAuthenticatedOrReadOnly(permissions.BasePermission):
    """
        Разрешение: авторизованные пользователи могут загружать материалы и голосовать,
        неавторизованные - только читать.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user