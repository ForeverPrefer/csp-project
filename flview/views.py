from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from upzy.models import Resource
from rsharing.models import Favorite

def new(request):
    """最新资源 - 按上传时间排序"""
    resources_list = Resource.objects.all().select_related('uploader').order_by('-upload_time')
    
    # 分页设置 - 每页6条
    paginator = Paginator(resources_list, 6)
    page = request.GET.get('page')
    
    try:
        resources = paginator.page(page)
    except PageNotAnInteger:
        resources = paginator.page(1)
    except EmptyPage:
        resources = paginator.page(paginator.num_pages)
    
    context = {
        'activmenu': 'flview',
        'resources': resources,
        'page_title': '最新资源',
        'page_subtitle': '发现最新上传的校园资源',
        'empty_icon': 'fa-clock',
        'empty_text': '暂无最新资源，快来分享你的第一个资源吧！',
    }
    return render(request, "new.html", context)

def down(request):
    """热门下载 - 按下载次数排序"""
    resources_list = Resource.objects.all().select_related('uploader').order_by('-download_count')
    
    # 分页设置 - 每页6条
    paginator = Paginator(resources_list, 6)
    page = request.GET.get('page')
    
    try:
        resources = paginator.page(page)
    except PageNotAnInteger:
        resources = paginator.page(1)
    except EmptyPage:
        resources = paginator.page(paginator.num_pages)
    
    context = {
        'activmenu': 'flview',
        'resources': resources,
        'page_title': '热门下载',
        'page_subtitle': '大家都在下载的热门资源',
        'empty_icon': 'fa-fire',
        'empty_text': '暂无热门下载资源，快来分享你的优质资源吧！',
    }
    return render(request, "down.html", context)

def xz(request):
    """精品推荐 - 下载数和收藏数都在前50的文件"""
    # 获取下载数前50的资源
    top_downloads = Resource.objects.all().order_by('-download_count')[:50]
    
    # 获取收藏数前50的资源（需要计算每个资源的收藏数）
    from django.db.models import Count
    top_favorites = Resource.objects.annotate(
        favorite_count=Count('favorite')
    ).order_by('-favorite_count')[:50]
    
    # 取交集：下载数前50且收藏数前50
    download_ids = set(top_downloads.values_list('id', flat=True))
    favorite_ids = set(top_favorites.values_list('id', flat=True))
    intersection_ids = download_ids.intersection(favorite_ids)
    
    # 获取交集资源
    resources_list = Resource.objects.filter(
        id__in=intersection_ids
    ).select_related('uploader').order_by('-upload_time')
    
    # 分页设置 - 每页6条
    paginator = Paginator(resources_list, 6)
    page = request.GET.get('page')
    
    try:
        resources = paginator.page(page)
    except PageNotAnInteger:
        resources = paginator.page(1)
    except EmptyPage:
        resources = paginator.page(paginator.num_pages)
    
    context = {
        'activmenu': 'flview',
        'resources': resources,
        'page_title': '精品推荐',
        'page_subtitle': '下载数和收藏数双重认证的优质资源',
        'empty_icon': 'fa-gem',
        'empty_text': '暂无精品资源，快来上传你的优质资源吧！',
    }
    return render(request, "xz.html", context)