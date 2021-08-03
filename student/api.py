from .serializers import AddClassSerializer, StudentRegistrationSerializer, StudentUpdateSerializer
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from .models import StudentClass, User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


class CustomAuthToken(ObtainAuthToken):
    """
    custom auth token
    """

    # serializer_class = AuthCustomTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # profile_picture = serializer.validated_data['profile_picture']
        token, created = Token.objects.get_or_create(user=user)
        user = User.objects.get(pk=user.id)

        response = {
            "data": {
                'token': token.key,
                'user_id': user.pk,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        }
        response['status'] = {"status": "User logged in successfully."}
        return Response(response)


class AddClassApi(viewsets.ModelViewSet):
    serializer_class = AddClassSerializer
    pagination_class = PageNumberPagination
    queryset = StudentClass.objects.all()


class RegistrationApi(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = StudentRegistrationSerializer
    pagination_class = PageNumberPagination
    queryset = User.objects.filter(is_superuser=False)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        serializer = StudentRegistrationSerializer
        if self.action == "update":
            serializer = StudentUpdateSerializer
        return serializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serialized = self.serializer_class(data=request.data, context={'request': request})
        if serialized.is_valid(raise_exception=True):
            user = serialized.create(validated_data=serialized.data)
            serialized = self.serializer_class(user)
            response = serialized.data
            response['success_message_head'] = "Successfully Created"
            return Response(response, status=201)