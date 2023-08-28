from django.urls import path
from .views import(
    RegisterView,
    LoginView,
    LogoutView,
    ProfileView,
    ProfileEditView,
)     



app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('profile/edit/', ProfileEditView.as_view(), name='profile-edit')
]
