from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.api.serializers import UserSerializer, UserDetailSerializer
from .permissions import IsAdminUserCustom
from rest_framework_simplejwt.backends import TokenBackend


@api_view(['GET', 'POST'])
@permission_classes((IsAdminUserCustom, ))
def user_api_view(request):
    if request.method == 'GET':
        # queryset
        users = User.objects.all()
        users_serializer = UserDetailSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # create
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario creado correctamente!'}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def user_detail_api_view(request, id=None):

    # get id from jwt obtained from headers
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
    user_id = valid_data['user_id']
    # query permissions from user id obtained from token
    user_is_staff = User.objects.filter(id=user_id).first().is_staff

    # if user obtained from token is admin, it can acces to any user data, else only can access to its own info
    if user_is_staff or user_id == id:
        user = User.objects.filter(id=id).first()
    else:
        return Response({'message': 'No tiene los permisos necesarios'}, status=status.HTTP_401_UNAUTHORIZED)

    # validation
    if user:
        # retrieve
        if request.method == 'GET':
            user_serializer = UserDetailSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        # update
        elif request.method == 'PUT':
            user_serializer = UserSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'message': 'Usuario actualizado correctamente'}, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # delete
        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': 'Usuario Eliminado correctamente!'}, status=status.HTTP_200_OK)

    return Response({'message': 'No se ha encontrado un usuario con estos datos'}, status=status.HTTP_400_BAD_REQUEST)
