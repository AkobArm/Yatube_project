from django.core.paginator import Paginator
from django.conf import settings


def get_page_context(post_list, request):
    paginator = Paginator(post_list,
                          settings.OBJECTS_PER_PAGE)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
