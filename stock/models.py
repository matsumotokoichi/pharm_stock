from django.db import models
from accounts.models import User, InstitutionCode

CATEGORY = (('1', '慢性疾患'), ('2', '感冒薬'), ('3', '漢方薬'), ('4','その他')) #薬学上は正しくない分類。現場で用いる分類を基準にカテゴライズ。

class Medicine(models.Model):
    
    institution_code_fk = models.ForeignKey(InstitutionCode, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    category = models.CharField(max_length=50,
                                choices=CATEGORY)
    stock = models.CharField(max_length=100) #--錠, --ml, --g 等単位が統一されていないのでcharfieldsで指定
    memo = models.TextField()
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'medicine'
        ordering = ('category', 'name' )

        
    def __str__(self):
        return self.name
