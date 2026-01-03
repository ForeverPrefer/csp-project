from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Resource

@login_required
def upzy(request):
    if request.method == 'POST':
        resource_name = request.POST.get('resource_name')
        resource_type = request.POST.get('resource_type')
        resource_file = request.FILES.get('resource_file')
        resource_desc = request.POST.get('resource_desc', '')
        
        if not all([resource_name, resource_type, resource_file]):
            messages.error(request, "资源名称、分类和文件不能为空！")
            return redirect('upzy:upzy')  
        
        try:
            Resource.objects.create(
                resource_name=resource_name,
                resource_type=resource_type,
                resource_file=resource_file,
                resource_desc=resource_desc,
                uploader=request.user
            )
            messages.success(request, "资源上传成功！")
            return redirect('upzy:upzy') 
        except Exception as e:
            messages.error(request, f"上传失败：{str(e)}")
            return redirect('upzy:upzy')  
    
    return render(request, 'upzy.html', {'activmenu': 'upzy'})