from django.urls import path
from .views import *

urlpatterns = [
    path('',HomePage,name='home'),
    path('signup/',Sign_up,name='sign_up'),
    path('<int:test_id>/ready_to_test/',Ready_to_test,name='ready_to_test'),
    path('<int:test_id>/test/',TestView,name='test'),
    path('<int:checktest_id>/checktest/',CheckTestView,name='checktest'),

]
