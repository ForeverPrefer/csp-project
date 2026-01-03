from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from upzy.models import Resource
from rsharing.models import Favorite
from .models import DownloadHistory

@login_required
def wdzy(request):
    """我的资源页面"""
    resources_list = Resource.objects.filter(uploader=request.user).order_by('-upload_time')
    
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
        'activmenu': 'self',
        'resources': resources,
        'current_section': 'my_resources'
    }
    return render(request, 'wdzy.html', context)  

@login_required
def wdxz(request):
    """我的下载页面"""
    downloads_list = DownloadHistory.objects.filter(user=request.user).select_related('resource').order_by('-downloaded_at')
    
    # 分页设置 - 每页4条
    paginator = Paginator(downloads_list, 4)
    page = request.GET.get('page')
    
    try:
        downloads = paginator.page(page)
    except PageNotAnInteger:
        downloads = paginator.page(1)
    except EmptyPage:
        downloads = paginator.page(paginator.num_pages)
    
    context = {
        'activmenu': 'self',
        'downloads': downloads,
        'current_section': 'download_history'
    }
    return render(request, 'wdxz.html', context)  

@login_required
def sc(request):
    """收藏夹页面"""
    favorites_list = Favorite.objects.filter(user=request.user).select_related('resource').order_by('-created_at')
    
    # 分页设置 - 每页6条
    paginator = Paginator(favorites_list, 6)
    page = request.GET.get('page')
    
    try:
        favorites = paginator.page(page)
    except PageNotAnInteger:
        favorites = paginator.page(1)
    except EmptyPage:
        favorites = paginator.page(paginator.num_pages)
    
    context = {
        'activmenu': 'self',
        'favorites': favorites,
        'current_section': 'favorites'
    }
    return render(request, 'sc.html', context)

@login_required
def sz(request):
    """账户设置页面"""
    user = request.user
    from django.contrib import messages  # 移到顶部
    
    if request.method == 'POST':
        has_changes = False  # 标记是否有实际修改
        password_changed = False  # 标记密码是否修改成功
        
        # 处理账户信息更新
        display_name = request.POST.get('display_name')
        email = request.POST.get('email')
        real_name = request.POST.get('real_name')
        
        # 检查基本信息是否有修改
        if display_name and display_name != user.display_name:
            user.display_name = display_name
            has_changes = True
        if email and email != user.email:
            user.email = email
            has_changes = True
        if real_name and real_name != user.real_name:
            user.real_name = real_name
            has_changes = True
        
        # 处理密码修改
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # 只有当所有密码字段都有值时才尝试修改密码
        if current_password and new_password and confirm_password:
            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    has_changes = True
                    password_changed = True
                    messages.success(request, '密码修改成功')
                else:
                    messages.error(request, '新密码和确认密码不匹配')
            else:
                messages.error(request, '当前密码错误')
        
        # 只有在有实际修改时才保存和显示成功消息
        if has_changes:
            user.save()
            if not password_changed:  # 如果不是密码修改的成功消息
                messages.success(request, '账户信息更新成功')
        else:
            if any([current_password, new_password, confirm_password]):
                # 用户尝试修改密码但失败了
                pass
            else:
                messages.info(request, '未检测到任何修改')
    
    context = {
        'activmenu': 'self',
        'current_section': 'account_settings',
        'user': user
    }
    return render(request, 'sz.html', context)