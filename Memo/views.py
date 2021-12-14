from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
from rest_framework.views import APIView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, MemoSerializer
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .models import Memo, Department

from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Electronic memorandum')

urlpatterns = [
    url(r'^$', schema_view)
]

# Register API


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": Token.objects.create(user=user).key
        })


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
                         'username': user.username,
                         'firstname': user.first_name,
                         'lastname': user.last_name,
                         'isadmin': user.is_superuser,
                         'dept': user.users.department.name}, status=200)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request):
        logout(request)
        return Response(status=200)


class MemoView(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = MemoSerializer

    def get_queryset(self):
        # TODO
        queryset = Memo.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data
        new_memo = Memo.objects.create(
            title=data["title"], body=data["body"], sender=request.user)
        new_memo.save()

        for receiver in data["receivers"]:
            dept_obj = Department.objects.get(id=receiver["id"])
            new_memo.receivers.add(dept_obj)

        serializer = MemoSerializer(new_memo)

        return Response(serializer.data)


class CreatedMemo(generics.ListAPIView):
    serializer_class = MemoSerializer

    def get(self, request, format=None):
        memos = Memo.objects.filter(
            sender__username=self.request.user.username)
        serializer = MemoSerializer(memos, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     serializer = MemoSerializer(
    #         data=request.data, sender=request.user.users)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    # queryset = Memo.objects.all()
    # serializer_class = MemoSerializer

    # def perform_create(self, serializer):
    #     serializer.save(sender=self.request.user)
