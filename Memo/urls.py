from .views import RegisterAPI, LoginView, LogoutView, MemoView, CreatedMemo
from django.urls import path, include
from rest_framework.authtoken import views as Token_views
urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/memo/', MemoView.as_view({'get': 'list',
                                        'post': 'create'}), name='memo'),
    path('api/memo/<int:pk>', MemoView.as_view({'get': 'retrieve',
                                                'put': 'update',
                                                'patch': 'partial_update',
                                                'delete': 'destroy'}), name='single'),
    path('api/memo/created', CreatedMemo.as_view(), name='create')
]
