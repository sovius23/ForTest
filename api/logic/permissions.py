from rest_framework import permissions
from api.models import Article


class IsArticleOwnerPermission(permissions.BasePermission):
    message = 'Упс, вы не имеете прав изменять статью!'
    def has_permission(self, request, view):
        try:
            self.message="Упс, похоже статьи не существует!"
            article=Article.objects.get(id = view.kwargs["pk"])
        except:
            return False
        return article.profile == request.user or request.user.is_superuser

class IsWriterPermission(permissions.BasePermission):
    message = 'Для добавления статей станьте автором!'
    def has_permission(self, request, view):
        return request.user.is_author