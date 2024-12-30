from django.urls import path
from users.views import user_login, user_logout, user_register, user_profile

urlpatterns = [
    path('login/', view=user_login, name='login'),
    path('register/', view=user_register, name='register'),
    path('profile/', view=user_profile, name='profile'),
    path('logout/', view=user_logout, name='logout'),
]