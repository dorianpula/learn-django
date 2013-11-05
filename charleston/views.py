from django.shortcuts import render_to_response, get_object_or_404
from charleston.models import Entry


def entries_index(request):
    return render_to_response('charleston/entry_index.html', {'entry_list': Entry.objects.all()} )


def entries_detail(request, year, month, day, slug):
    import datetime
    import time

    # Icky... datetime parsing.
    date_stamp = time.strptime(year+month+day, "%Y%b%d")
    pub_date = datetime.date(*date_stamp[:3])

    entry = get_object_or_404(Entry,
                              publication_date__year=pub_date.year,
                              publication_date__month=pub_date.month,
                              publication_date__day=pub_date.day,
                              slug=slug)

    return render_to_response('charleston/entry_detail.html', {'entry': entry})
