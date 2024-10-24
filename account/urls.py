from django.urls import path
from .views import RegisterUserView, LoginUserView, UserDetailView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
]
