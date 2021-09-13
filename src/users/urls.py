from django.urls import path

from users.viewsets import LoginAPIView, LogoutAPIView, UserSignUpAPIView

app_name = 'users'
urlpatterns = [
    path('signup/', UserSignUpAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
