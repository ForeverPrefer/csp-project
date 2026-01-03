from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm

def register_view(request):
    # 如果用户已登录，直接跳转到首页或next参数指定的页面
    if request.user.is_authenticated:
        next_url = request.GET.get('next', '/')
        return redirect(next_url)
    
    login_form = LoginForm()
    register_form = RegisterForm()
    
    # 处理登录
    if request.method == 'POST' and 'login_submit' in request.POST:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            phone = login_form.cleaned_data['phone']
            password = login_form.cleaned_data['password']
            remember_me = login_form.cleaned_data['remember_me']
            
            user = authenticate(request, phone=phone, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                messages.success(request, '登录成功！')
                next_url = request.POST.get('next') or request.GET.get('next') or '/'
                return redirect(next_url)
            else:
                messages.error(request, '手机号或密码错误！')
    
    # 处理注册
    elif request.method == 'POST' and 'register_submit' in request.POST:
        print("=== 注册请求开始 ===")
        print("POST数据:", request.POST)
        
        register_form = RegisterForm(request.POST)
        print("表单是否绑定:", register_form.is_bound)
        print("表单是否有效:", register_form.is_valid())
        
        if not register_form.is_valid():
            print("表单错误详情:")
            for field, errors in register_form.errors.items():
                print(f"字段 {field}: {errors}")
            
            # 显示错误消息
            for field, errors in register_form.errors.items():
                for error in errors:
                    # 获取字段的友好名称
                    if field in register_form.fields:
                        field_name = register_form.fields[field].label
                    else:
                        field_name = field
                    messages.error(request, f'{field_name}: {error}')
        else:
            print("表单验证通过，开始创建用户...")
            try:
                user = register_form.save(commit=False)
                # 如果没有设置显示名称，使用手机号
                if not user.display_name:
                    user.display_name = user.phone
                user.save()
                print(f"用户创建成功: {user.phone}")
                
                login(request, user)
                messages.success(request, '注册成功!欢迎使用CSP校园资源分享平台')
                
                next_url = request.POST.get('next') or request.GET.get('next') or '/'
                return redirect(next_url)
                
            except Exception as e:
                print(f"用户创建异常: {str(e)}")
                messages.error(request, f'注册失败: {str(e)}')
        
        print("=== 注册请求结束 ===")
    
    context = {
        'login_form': login_form,
        'register_form': register_form,
        'next': request.GET.get('next', '')
    }
    return render(request, "register.html", context)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, '您已成功退出登录')
    return redirect('home:home')