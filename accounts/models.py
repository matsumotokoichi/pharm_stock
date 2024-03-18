from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class InstitutionCode(models.Model):
    institution_name = models.CharField(max_length=20)
    code = models.CharField(max_length=5) # P-----:薬局 C-----:病院
    
    class Meta:
        db_table = 'institutioncode'
        ordering = ('institution_name', )
        
    def __str__(self):
        return self.institution_name
    
    
    
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email!')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.create_at = datetime.now()
        user.update_at = datetime.now()
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
    # 必要なCategoryインスタンスを作成または取得
        code = InstitutionCode.objects.create(institution_name="管理者", code="P9999")
        user = self.model(
            username=username,
            email=email,
            institution_code = code
        )
        user.create_at = datetime.now()
        user.update_at = datetime.now()
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user    
    

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20)
    email = models.EmailField(unique=True) 
    institution_name = models.CharField(max_length=50, null=True)
    institution_code = models.ForeignKey(InstitutionCode, on_delete=models.CASCADE)
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']
        
    class Meta:
        db_table = 'user'
        
    def __str__(self):
        return self.institution_name
     
    def clean(self):
    
        super().clean()

        # このユーザー以外で同じメールアドレスを持つユーザーがいるかチェック
        existing_users = User.objects.exclude(pk=self.pk).filter(email=self.email)

        if existing_users.exists():
            # メールアドレスが他のユーザーと重複している場合はエラーを発生させる
            raise ValidationError({'email': _('このメールアドレスはに使用されています')})