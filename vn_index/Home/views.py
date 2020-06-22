from django.shortcuts import render
from . import get_index
from .get_data_detail import GetDataDetail
from .system import check_newwork
from .models import Link


def Homepage(request):
    if not check_newwork():
        return "Please check network connection"
    if request.method == "GET":
        cpn_code = request.GET.get('cpn_code')
        if cpn_code:
            link = f"https://s.cafef.vn/hose/{cpn_code.upper()}-.chn"
            index = get_index.GetIndex(link).get_all_index_info().to_html(classes='table table-striped table-fixed') \
                if get_index.GetIndex(link).get_all_index_info() is not None else None
            data = GetDataDetail().crawl_all_data(cpn_code).to_html(classes='table table-striped table-fixed') \
                if GetDataDetail().crawl_all_data(cpn_code) is not None else None

            return render(request, 'homepage.html', {'link': link, 'index': index,
                                                     'data': data})
    return render(request, 'homepage.html')

