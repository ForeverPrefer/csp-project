from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['phone', 'email', 'display_name', 'real_name']

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['phone', 'email', 'display_name', 'real_name', 'is_active', 'is_staff']

class LoginForm(forms.Form):
    phone = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入手机号'
        }),
        label='手机号'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码'
        }),
        label='密码'
    )
    remember_me = forms.BooleanField(required=False, label='记住我')

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请设置密码'
        }),
        label='密码',
        help_text='密码长度至少8位,包含字母和数字'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': '请确认密码'
        }),
        label='确认密码'
    )
    
    class Meta:
        model = CustomUser
        fields = ['phone', 'email', 'display_name', 'real_name']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请设置手机号'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入邮箱'
            }),
            'display_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请设置用户名'
            }),
            'real_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入真实姓名'
            }),
        }
        labels = {
            'phone': '手机号',
            'email': '邮箱',
            'display_name': '用户名',
            'real_name': '真实姓名',
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone:
            raise ValidationError('手机号不能为空')
        if not phone.isdigit() or len(phone) != 11:
            raise ValidationError('手机号必须为11位数字')
        
        # 检查手机号是否已存在
        if CustomUser.objects.filter(phone=phone).exists():
            raise ValidationError('该手机号已被注册')
        
        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('邮箱不能为空')
        
        # 检查邮箱是否已存在
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('该邮箱已被注册')
        
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("两次输入的密码不一致")
        
        # 密码强度验证
        if len(password1) < 8:
            raise ValidationError("密码长度至少8位")
        if password1.isdigit():
            raise ValidationError("密码不能全是数字")
        if password1.isalpha():
            raise ValidationError("密码不能全是字母")
            
        return password2