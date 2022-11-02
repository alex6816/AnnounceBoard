from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *


urlpatterns = [
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('signup/', BaseRegisterView.as_view(), name='signup'),
    path('signup/code_enter/', code_enter, name='code_enter'),
    path('signup/verify/', verify, name='verify')

]