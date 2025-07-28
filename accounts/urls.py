from django.urls import path
from .views import RegisterView, CustomLoginView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', CustomLoginView.as_view()),
    path('users/', UserListView.as_view()),
]
