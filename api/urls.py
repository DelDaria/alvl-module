from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import IssueViewSet, CommentViewSet, CustomAuthToken, ExampleView


router = DefaultRouter()
router.register(r'issues', IssueViewSet, basename='issues')
router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = router.urls

urlpatterns += [
    path('api-token-auth/',  CustomAuthToken.as_view()),
    path('example/', ExampleView.as_view()),

]
