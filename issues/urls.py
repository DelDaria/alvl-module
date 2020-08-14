from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateIssueView.as_view(), name='create_issue'),
    path('issues/<int:pk>', views.IssueDetail.as_view(), name='issue_detail'),
    path('new_issues/', views.NewIssueList.as_view(), name='new_issues'),
    path('issues/edit/<int:pk>', views.IssueUpdate.as_view(), name='edit_issue'),
    path('comment/<int:pk>/new', views.NewCommentView.as_view(), name='new_comment'),

]
