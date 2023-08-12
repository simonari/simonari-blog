from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # posts views
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>',
         views.PostDetailView.as_view(), name='post_detail'),
    path('new-post', views.PostCreateView.as_view(), name='post_create'),

    # drafts views
    path('draft', views.DraftListView.as_view(), name='draft_list'),
    path('draft/<int:year>/<int:month>/<int:day>/<slug:draft>',
         views.DraftDetailView.as_view(), name='draft_detail'),
]
