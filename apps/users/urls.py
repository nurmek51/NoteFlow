from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, UserDetailView, UserFavoriteLecturerUpdateDeleteView, \
    UserFavoriteSubjectsUpdateDeleteView, ProfilePictureUploadView, ProfilePictureDeleteView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   #post
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  #post
    path('register/', UserRegistrationView.as_view(), name='register_user'),   #post
    path('user/detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),  #get-details(even favorite), put-change details, delete-deleteuser
    path('user/favorite_lecturer/', UserFavoriteLecturerUpdateDeleteView.as_view(), name='user_favorite_lecturer'),  #CHANGE AND DELETE FAV.LECTURER
    path('user/favorite_subjects/', UserFavoriteSubjectsUpdateDeleteView.as_view(), name='user_favorite_subjects'),  #APPEND AND DELETE SUBJECTS FROM FAV.LIST
    path('user/profile_picture/upload/', ProfilePictureUploadView.as_view(), name='user_profile_picture_upload'),  #UPLOAD avatar and update
    path('user/profile_picture/delete/', ProfilePictureDeleteView.as_view(), name='user_profile_picture_delete'),  #delete avatar
]