from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, email, password=None, **extra_fields):
        if not phone:
            raise ValueError('用户必须提供手机号')
        if not email:
            raise ValueError('用户必须提供邮箱')
        
        email = self.normalize_email(email)
        user = self.model(phone=phone, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置 is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置 is_superuser=True')
        
        return self.create_user(phone, email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None
    
    phone = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    email = models.EmailField(unique=True, verbose_name="邮箱")
    
    display_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="显示名称")
    real_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="真实姓名")
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']
    
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
    
    def __str__(self):
        return self.display_name or self.phone

    def clean(self):
        if not self.phone.isdigit() or len(self.phone) != 11:
            raise ValidationError('手机号必须为11位数字')

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = self.phone
        self.full_clean()
        super().save(*args, **kwargs)
        
    def get_display_name(self):
        if self.display_name and self.display_name != self.phone:
            return self.display_name
        return self.phone