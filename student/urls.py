from django.urls import path, include
from rest_framework import routers
from student import api as v1_api


router = routers.DefaultRouter()
router.register(r'class', v1_api.AddClassApi, basename='class')
router.register(r'registration', v1_api.RegistrationApi, basename='registration')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/login/', v1_api.CustomAuthToken.as_view()),

]
