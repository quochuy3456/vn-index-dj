from django.shortcuts import render
from . import get_index
from .get_data_detail import gd
from .models import Link


def Homepage(request):
    if request.method == "POST":
        cpn_code = request.POST.get('cpn_code')
        if cpn_code:
            link = Link.objects.get(code=cpn_code).link
            index = get_index.GetIndex(link).get_list().to_html(classes='table table-striped table-fixed')
            data = gd.crawl_all_data(cpn_code).to_html(classes='table table-striped table-fixed')
            return render(request, 'homepage.html', {'link':link, 'index': index, 'data': data})
    return render(request, 'homepage.html')
