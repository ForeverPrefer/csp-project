import os
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from CSP.utils import paginate
from upzy.models import Resource
from .models import Favorite

@login_required
def resource_detail(request, resource_id):
    """资源详情页面"""
    resource = get_object_or_404(Resource.objects.select_related('uploader'), id=resource_id)
    
    # 获取相关资源（同类型的其他资源）
    related_resources = Resource.objects.filter(
        resource_type=resource.resource_type
    ).exclude(id=resource.id).select_related('uploader').order_by('-download_count')[:3]
    
    # 获取文件信息
    file_info = {
        'name': os.path.basename(resource.resource_file.name),
        'size': resource.resource_file.size,
        'format': os.path.splitext(resource.resource_file.name)[1].upper().replace('.', ''),
        'upload_time': resource.upload_time,
    }
    
    # 检查用户是否已收藏该资源 - 使用正确的查询方式
    is_favorited = False
    favorite_count = 0
    
    if request.user.is_authenticated:
        # 使用字符串引用方式查询
        from rsharing.models import Favorite
        is_favorited = Favorite.objects.filter(
            user=request.user, 
            resource=resource
        ).exists()
    
    # 获取收藏数量
    favorite_count = Favorite.objects.filter(resource=resource).count()
    
    context = {
        'resource': resource,
        'resources': related_resources,
        'file_info': file_info,
        'activmenu': 'rsharing',
        'is_favorited': is_favorited,
        'favorite_count': favorite_count,
    }
    return render(request, 'resource_detail.html', context)

@login_required
def download_resource(request, resource_id):
    resource = get_object_or_404(Resource, id=resource_id)
    if not resource.resource_file:
        raise Http404("文件不存在")
    
    resource.download_count += 1
    resource.save()
    
    # 记录下载历史
    if request.user.is_authenticated:
        from self.models import DownloadHistory
        DownloadHistory.objects.create(user=request.user, resource=resource)
    
    file_path = resource.resource_file.path
    filename = os.path.basename(file_path)
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def resource_list(request, resource_type):
    """通用资源列表视图，根据参数过滤数据"""
    type_config = {
        '文档资料': {
            'title': '文档资料',
            'subtitle': '共享学习文档、笔记、资料等',
            'empty_icon': 'fa-file-alt',
            'empty_text': '还没有人上传文档资料，快来分享你的第一份资料吧！',
            'index': 1,
        },
        '软件工具': {
            'title': '软件工具',
            'subtitle': '实用的软件和工具资源',
            'empty_icon': 'fa-tools',
            'empty_text': '还没有人上传软件工具，快来分享你的第一个工具吧！',
            'index': 2,
        },
        '学习教程': {
            'title': '学习教程',
            'subtitle': '各类学习教程和课程资料',
            'empty_icon': 'fa-graduation-cap',
            'empty_text': '还没有人上传学习教程，快来分享你的第一个教程吧！',
            'index': 3,
        },
        '模板资源': {
            'title': '模板资源',
            'subtitle': '各类文档模板和设计资源',
            'empty_icon': 'fa-copy',
            'empty_text': '还没有人上传模板资源，快来分享你的第一个模板吧！',
            'index': 4,
        }
    }

    # 获取当前资源类型的配置
    config = type_config.get(resource_type, type_config['文档资料'])
    
    resources_list = Resource.objects.filter(
        resource_type=resource_type
    ).select_related('uploader').order_by('-upload_time')
    resources = paginate(request, resources_list, 6)
    return render(request, 'resource_list.html', {
        'resources': resources,
        'activmenu': 'rsharing',
        'resource_title': config['title'],
        'resource_subtitle': config['subtitle'],
        'empty_icon': config['empty_icon'],
        'empty_text': config['empty_text'],
        'carousel_index': config['index'],
        'resource_type': resource_type,
    })


@login_required
def toggle_favorite(request, resource_id):
    if request.method == 'POST':
        try:
            resource = Resource.objects.get(id=resource_id)
            favorite, created = Favorite.objects.get_or_create(
                user=request.user,
                resource=resource
            )
            
            if not created:
                # 如果已经收藏过，则取消收藏
                favorite.delete()
                action = 'removed'
            else:
                action = 'added'
            
            # 获取更新后的收藏数量
            favorite_count = Favorite.objects.filter(resource=resource).count()
            
            return JsonResponse({
                'status': 'success',
                'action': action,
                'favorite_count': favorite_count
            })
            
        except Resource.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': '资源不存在'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': '无效的请求'
    })