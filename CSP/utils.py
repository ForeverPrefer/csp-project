from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paginate(request, queryset, per_page=6):
    """统一分页，返回当前页的 Page 对象。

    Args:
        request: HttpRequest，从中读取 page 参数。
        queryset: 待分页的 QuerySet。
        per_page: 每页条数，默认 6。
    """
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)
