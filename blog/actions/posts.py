from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from ..models import Post

STATUS_TO_SLUG = {
    'posted': 'post',
    'drafted': 'draft'
}

STATUS_ANTIPODES = {
    'posted': 'drafted',
    'drafted': 'posted'
}


def _get_post(request, year, month, day, status, slug):
    obj = get_object_or_404(Post,
                            slug=slug,
                            status=status,
                            published__year=year,
                            published__month=month,
                            published__day=day)

    return obj


def delete_post(request, year, month, day, status, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/blog/login")

    obj = _get_post(request, year, month, day, status, slug)
    obj_status = obj.status
    redirect_to = '/blog' if obj_status == 'posted' else '/blog/draft'
    obj.delete()

    return HttpResponseRedirect(redirect_to)


def edit_post(request, year, month, day, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/blog/login")


def change_post_status(request, year, month, day, status, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/blog/login")

    obj = _get_post(request, year, month, day, status, slug)

    status_to_set = STATUS_ANTIPODES.get(obj.status)

    if not status_to_set:
        raise ValueError(f'Status {obj.status} can not be changed')

    obj.status = status_to_set
    obj.save()

    redirect_to = obj.get_absolute_url()

    return HttpResponseRedirect(redirect_to)
