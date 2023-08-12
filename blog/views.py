from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from .models import Post
from .forms import DraftDetailUpdateForm


class DraftListView(ListView):
    queryset = Post.objects.filter(status='draft')
    context_object_name = "drafts"

    paginate_by = 5
    template_name = 'blog/draft/list.html'


class DraftDetailView(UpdateView):
    model = Post
    context_object_name = "draft"
    form_class = DraftDetailUpdateForm
    template_name = 'blog/draft/detail.html'
    success_url = None
    object = None

    def get_object(self, **kwargs):
        obj = get_object_or_404(Post,
                                slug=self.kwargs['draft'],
                                status='draft',
                                published__year=self.kwargs['year'],
                                published__month=self.kwargs['month'],
                                published__day=self.kwargs['day'])
        self.object = obj
        return obj

    def form_valid(self, form):
        self.object.status = 'published'
        self.object.save()
        self.success_url = self.object.get_absolute_url()
        return HttpResponseRedirect(self.success_url)


    # def btn_publish(self):
    #     obj = get_object_or_404(Post,
    #                             slug=self.kwargs['draft'],
    #                             status='draft',
    #                             published__year=self.kwargs['year'],
    #                             published__month=self.kwargs['month'],
    #                             published__day=self.kwargs['day'])
    #
    #     obj.status = 'published'
    #     obj.save()
    #     redirect(obj.get_absolute_url())


class PostListView(ListView):
    queryset = Post.publish.all()
    context_object_name = 'posts'

    paginate_by = 5
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


# TODO inherit from EditView
class PostEditView:
    ...
