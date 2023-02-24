from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS') - если метод безопасный
        if request.method in permissions.SAFE_METHODS:
            # True - права доступа предоставлены, False - нет
            return True
        # Проверка на админа
        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Если юзер из БД равен пользователю из запроса
        return obj.user == request.user
