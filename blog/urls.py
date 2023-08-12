from django.urls import path
from . import views
from .actions import posts

app_name = 'blog'

urlpatterns = [
    # Published posts views
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>',
         views.PostDetailView.as_view(), name='post_detail'),

    # Drafted posts views
    path('draft', views.DraftListView.as_view(), name='draft_list'),
    path('draft/<int:year>/<int:month>/<int:day>/<slug:draft>',
         views.DraftDetailView.as_view(), name='draft_detail'),

    # View to create post
    path('new-post', views.PostCreateView.as_view(), name='post_create'),

    # Actions with posts
    path('delete_post/<int:year>/<int:month>/<int:day>/<str:status>/<str:slug>',
         posts.delete_post, name='delete_post'),
    path('change_post_status/<int:year>/<int:month>/<int:day>/<str:status>/<str:slug>',
         posts.change_post_status, name='change_post_status')
]
