from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from CSP.utils import paginate
from upzy.models import Resource

def home(request):
    """首页视图 - 在首页直接分页显示搜索结果"""
    query = request.GET.get('q', '').strip()

    # 获取统计数据（无论是否搜索都需要）
    total_resources = Resource.objects.count()
    total_downloads = Resource.objects.aggregate(total=Sum('download_count'))['total'] or 0
    
    # 如果有搜索查询，执行搜索并分页
    if query:
        search_results = Resource.objects.filter(
            Q(resource_name__icontains=query) |
            Q(resource_desc__icontains=query) |
            Q(uploader__display_name__icontains=query) |
            Q(uploader__phone__icontains=query)
        ).select_related('uploader').order_by('-upload_time')
        
        total_results = search_results.count()
        search_results_page = paginate(request, search_results, 6)
        
        context = {
            'activmenu': 'home',
            'search_query': query,
            'search_results': search_results_page,
            'total_results': total_results,
            'show_search_results': True,
            'has_results': total_results > 0,
            # 搜索时也要传递统计数据
            'total_resources': total_resources,
            'total_downloads': total_downloads,
        }
        
        return render(request, "home.html", context)
    
    # 如果没有搜索查询，显示正常首页
    latest_resources = Resource.objects.all().select_related('uploader').order_by('-upload_time')[:4]
    popular_resources = Resource.objects.all().select_related('uploader').order_by('-download_count')[:4]
    
    premium_resources = Resource.objects.annotate(
        favorite_count=Count('favorite')
    ).filter(
        favorite_count__gt=0
    ).select_related('uploader').order_by('-upload_time')[:4]
    
    context = {
        'activmenu': 'home',
        'latest_resources': latest_resources,
        'popular_resources': popular_resources,
        'premium_resources': premium_resources,
        'total_resources': total_resources,
        'total_downloads': total_downloads,
        'search_query': query,
        'show_search_results': False,
        'has_results': True,
    }
    return render(request, "home.html", context)

def logout1(request):
    logout(request)
    return redirect('home:home')

@require_GET
def search_suggestions(request):
    """搜索建议API"""
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'results': []})
    
    results = Resource.objects.filter(
        Q(resource_name__icontains=query) |
        Q(resource_desc__icontains=query)
    ).select_related('uploader').order_by('-download_count')[:5]
    
    suggestions = []
    for resource in results:
        suggestions.append({
            'id': resource.id,
            'resource_name': resource.resource_name,
            'resource_desc': resource.resource_desc or '',
            'uploader': resource.uploader.get_display_name(),
            'download_count': resource.download_count,
            'resource_type': resource.resource_type
        })
    
    return JsonResponse({'results': suggestions})
