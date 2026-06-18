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
        register_form = RegisterForm(request.POST)
        
        if not register_form.is_valid():
            for field, errors in register_form.errors.items():
                for error in errors:
                    if field in register_form.fields:
                        field_name = register_form.fields[field].label
                    else:
                        field_name = field
                    messages.error(request, f'{field_name}: {error}')
        else:
            try:
                user = register_form.save(commit=False)
                if not user.display_name:
                    user.display_name = user.phone
                user.save()
                login(request, user)
                messages.success(request, '注册成功!欢迎使用CSP校园资源分享平台')
                next_url = request.POST.get('next') or request.GET.get('next') or '/'
                return redirect(next_url)
            except Exception as e:
                messages.error(request, f'注册失败: {str(e)}')
    
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