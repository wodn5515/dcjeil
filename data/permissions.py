from rest_framework import permissions

class CommentPermission(permissions.BasePermission):
    message = "권한이 없습니다."

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == "POST":
            self.message = "로그인 후 이용해주세요."
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.writer == request.user