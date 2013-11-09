"""
Views for the charleston project.

"""
from django.shortcuts import render_to_response, get_object_or_404

from charleston.models import Category


def category_list(request):
    """
    Render a list of categories.

    :param request: The request to render.
    """
    return render_to_response('charleston/category_list.html', {'object_list': Category.objects.all()})


def category_detail(request, slug):
    """
    Category details based on request or slug.

    :param request: The request to serve.
    :param slug: The slug for the category.
    """

    category = get_object_or_404(Category, slug=slug)
    return render_to_response('charleston/category_detail.html',
                              {'object_list': category.entry_set.all(),
                               'category': category})
