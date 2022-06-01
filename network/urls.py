from django.urls import path
from . import views

app_name = 'network'

urlpatterns = [
    path('woof/', views.WoofListAPIView.as_view(), name='woof-list'),

    path('following/', views.FollowingWoofListAPIView.as_view(),
         name='following-list'),

    path('woof/<str:username>', views.WoofByUsernameListAPIView.as_view(),
         name='woofbyuser-list'),

    path('woofupdate/<int:pk>',
         views.WoofUpdateAPIView.as_view(), name='woof-update'),

    path('wooflike/<int:pk>',
         views.WoofLikeAPIView.as_view(), name='woof-like'),
    path('woofunlike/<int:pk>',
         views.WoofUnlikeAPIView.as_view(), name='woof-unlike'),

    path('user/', views.UsersListAPIView.as_view(), name='user-list'),

    path('user/<str:username>', views.UserFilterListAPIView.as_view(),
         name='userfilter-list'),

    path('follow/<str:username>', views.UserFollowUpdateApiVIEW.as_view(),
         name='userfollow-list'),

    path('unfollow/<str:username>', views.UserUnfollowUpdateApiVIEW.as_view(),
         name='userfollow-list'),

    path('isfollowing/<str:username>', views.IsFollowingListAPIView.as_view(),
         name='isfollowing-list'),


    # Authentication paths
    # path('', views.getRoutes),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
