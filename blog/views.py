from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.utils.text import slugify
from .models import Post


class PostListView(ListView):
    queryset = Post.publish.all()
    context_object_name = 'posts'

    paginate_by = 3
    template_name = 'blog/post/list.html'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

    template_name = 'blog/post/detail.html'

    def get_object(self, **kwargs):
        obj = get_object_or_404(Post,
                                slug=self.kwargs['post'],
                                status='published',
                                published__year=self.kwargs['year'],
                                published__month=self.kwargs['month'],
                                published__day=self.kwargs['day'])

        return obj


class PostCreateView(CreateView):
    model = Post
    context_object_name = 'post_create'
    fields = ['title', 'author', 'body']
    template_name = 'blog/post/create.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        form.save()
        return super().form_valid(form)


def post_edit(request, year, month, day, post):
    ...
