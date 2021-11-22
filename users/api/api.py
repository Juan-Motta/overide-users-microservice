from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from users.models import User
from users.api.serializers import UserListSerializer, UserCreateSerializer, UserUpdateSerializer, UserUpdatePasswordSerializer
from rest_framework_simplejwt.backends import TokenBackend


@api_view(['GET'])
@permission_classes((IsAdminUser, ))
def user_all_api_view(request):
    """
    Obtains all users, only for admin users credentials
    """
    if request.method == 'GET':
        # queryset
        users = User.objects.all()
        users_serializer = UserListSerializer(users, many=True)
        return Response(users_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def user_create_api_view(request):
    """"
    Creates an user
    """
    if request.method == 'POST':
        # create
        user_serializer = UserCreateSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes((IsAuthenticated, ))
def user_by_id_api_view(request, id=None):
    """
    Lists, Updates and Deletes an user by id, only accessable by either an user itself or an admin user
    """

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
        return Response({'message': 'No tiene los permisos necesarios para realizar esta operación'}, status=status.HTTP_401_UNAUTHORIZED)

    # validation
    if user:
        # retrieve
        if request.method == 'GET':
            user_serializer = UserListSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)

        # update
        elif request.method == 'PUT':
            user_serializer = UserUpdateSerializer(user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'message': 'Usuario actualizado correctamente'}, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # delete
        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': 'Usuario Eliminado correctamente!'}, status=status.HTTP_200_OK)

    return Response({'message': 'No se ha encontrado un usuario con estos datos'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, ])
def user_update_password_api_view(request, id=None):
    """
    Updates a specific user password, only accessable by either an user itself or an admin user
    """
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

    if user:
        # update
        if request.method == 'PUT':
            user_serializer = UserUpdatePasswordSerializer(
                user, data=request.data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'message': 'Contraseña actualizada correctamente'}, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
