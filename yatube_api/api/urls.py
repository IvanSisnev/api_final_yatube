"""
Эндпоинты api.
"""
from rest_framework.routers import SimpleRouter
from django.urls import include, path

from api.views import PostViewSet, GroupViewSet, FollowViewSet, CommentViewSet

router = SimpleRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet, basename='follow')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comment')

urlpatterns = [
    path('v1/', include(router.urls))
]
