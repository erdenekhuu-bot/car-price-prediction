from django.db import models

# Create your models here.

class MashinData(models.Model):
    id = models.AutoField(primary_key=True)
    Niitelsen = models.CharField(max_length=100)
    Uildverlegch = models.CharField(max_length=100)
    Mark = models.CharField(max_length=100)
    Motor_bagtaamj = models.CharField(max_length=100)
    Xrop = models.CharField(max_length=100)
    Joloo = models.CharField(max_length=100)
    Torol = models.CharField(max_length=100)
    Ungu = models.CharField(max_length=100)
    Uildverlesen_on = models.IntegerField()
    Orj_irsen_on = models.IntegerField()
    Hudulguur = models.CharField(max_length=100)
    Dotor_ungu = models.CharField(max_length=100)
    Lizeng = models.CharField(max_length=100)
    Hayg = models.CharField(max_length=100, null=True, blank=True)
    Hutlugch = models.CharField(max_length=100)
    Yavsan_km = models.CharField(max_length=100)
    Nomer = models.CharField(max_length=100)
    Haalga = models.CharField(max_length=100)
    Une = models.IntegerField()
    Unique_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mashin_data'
    
    def __str__(self):
        return f'{self.Uildverlegch}, {self.Mark}, {self.Motor_bagtaamj}, {self.Xrop}, {self.Torol}, {self.Uildverlesen_on}, {self.Hudulguur}, {self.Hutlugch}, {self.Yavsan_km}'