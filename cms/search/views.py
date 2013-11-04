# Search app views

from django.http import HttpResponse
from django.template import loader, Context
from django.contrib.flatpages.models import FlatPage


def search(request):
    query = request.GET['q']

    # Get a set of all flatpage models, filtering on an extracted keyword match
    results = FlatPage.objects.filter(content__icontains=query)

    # Loads a template and setups the context of the call
    template = loader.get_template("search/search.html")
    context = Context({'query': query, 'results': results})

    # Render a response!
    response = template.render(context)
    return HttpResponse(response)

