from rest_framework import permissions

from apps.blog.models import Article


class ArticlePermissions(permissions.BasePermission):
    """
    Custom permission for django rest framework.
    """

    def has_permission(self, request, view):
        if view.action == 'create':
            return request.user.has_perm(Article.get_perm('add'))

        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user

        if view.action in ['update', 'partial_update']:
            return user.has_perm(Article.get_perm('change'), obj)

        elif view.action == 'destroy':
            return user.has_perm(Article.get_perm('delete'), obj)

        return True
