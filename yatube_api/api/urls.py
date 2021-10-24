from api.views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'posts', PostViewSet)
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet,
                basename='comment')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
