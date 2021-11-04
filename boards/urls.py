from django.urls import path
from . import views

urlpatterns = [
 path("", views.HomeView, name = "home"),
 path("boards/<int:pk>/", views.TopicsView, name='topics'),
 path("boards/<int:pk>/new/", views.NewTopicView, name='new_topic'),
 path("boards/<int:pk>/topics/<int:topic_pk>/", views.TopicPostView, name='topic_posts'),
 path("boards/<int:pk>/topics/<int:topic_pk>/reply/", views.ReplyTopicView, name='reply_topic'),
 path("boards/<int:pk>/topics/<int:topic_pk>/posts/<int:post_pk>/edit/", views.PostUpdateView.as_view(), name='edit_post'),
]


