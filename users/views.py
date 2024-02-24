""" Представления для users """
from rest_framework import viewsets
from users.models import User
from users.pagination import UserPagination
from users.permissions import UserPermission
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet для пользователей """
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('pk')
    permission_classes = [UserPermission]
    pagination_class = UserPagination

    def create(self, request, *args, **kwargs):
        # Переопределение метода create для разрешения создания пользователя всем
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
