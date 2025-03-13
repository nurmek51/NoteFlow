from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, UserDetailView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   #post
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  #post
    path('register/', UserRegistrationView.as_view(), name='register_user'),   #post
    path('user/detail/<int:pk>', UserDetailView.as_view(), name='user_detail')  #get-details, put-change details, delete-deleteuser
]

# {
#     "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MjI3NDUzNywiaWF0IjoxNzQxNjY5NzM3LCJqdGkiOiJjNDFlYTg1ZjllZDA0Zjg3YWI2ZjI3ZTcwYjJlNmEzNyIsInVzZXJfaWQiOjF9.jNyBrEvWKchxY57y-JM6eNkJVhuNPilmbNVfo45tnt4",
#     "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQxNzU2MTM3LCJpYXQiOjE3NDE2Njk3MzcsImp0aSI6IjA2NDBlZmY0NDhkZTRhOWM5YzU4NDBjNTE1MDQwMzM0IiwidXNlcl9pZCI6MX0.fAqRJOk1g2bBA_zQUjUL-Cv0j4RjSbDO67YJwW5LBMM"
# }