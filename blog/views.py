from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponseNotFound
from .models import Post, User
from .forms import DraftDetailUpdateForm, PostDetailUpdateForm

STATUS_TO_SLUG = {
    'posted': 'post',
    'drafted': 'draft'
}


class PostListView(ListView):
    queryset = Post.objects.filter(status='posted')
    context_object_name = 'posts'

    paginate_by = 5
    template_name = 'blog/post/list.html'


class DraftListView(ListView):
    queryset = Post.objects.filter(status='drafted')
    context_object_name = "drafts"

    paginate_by = 5
    template_name = 'blog/draft/list.html'


class BaseDetailView(UpdateView):
    model = Post

    context_object_name = None
    form_class = None
    template_name = None

    object = None
    object_status = None

    def get_object(self, queryset=None):
        slug = self._status_to_slug(self.object_status)

        obj = get_object_or_404(Post,
                                slug=slug,
                                status=self.object_status,
                                published__year=self.kwargs['year'],
                                published__month=self.kwargs['month'],
                                published__day=self.kwargs['day'])
        self.object = obj
        return obj

    def _status_to_slug(self, status):
        slug = STATUS_TO_SLUG.get(status)

        if slug is None:
            raise ValueError(f'Status {status} is invalid')

        return self.kwargs[slug]


class DraftDetailView(BaseDetailView):
    context_object_name = "post"
    form_class = DraftDetailUpdateForm
    template_name = 'blog/draft/detail.html'

    object_status = 'drafted'


class PostDetailView(BaseDetailView):
    context_object_name = 'post'
    form_class = PostDetailUpdateForm
    template_name = 'blog/post/detail.html'

    object_status = 'posted'


class PostCreateView(CreateView):
    model = Post
    context_object_name = 'post_create'
    fields = ['title', 'body']
    template_name = 'blog/post/create.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        # TODO past user's profile after authorization
        form.instance.author = User.objects.get(username='admin')
        form.save()
        return super().form_valid(form)


# TODO inherit from EditView
class PostEditView:
    ...
