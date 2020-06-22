from django.db import models

# Create your models here.


class Link(models.Model):
    code = models.CharField(max_length=5)
    link = models.CharField(max_length=200)

    def __str__(self):
        return self.code


class CpnInfo(models.Model):
    cpn_id = models.IntegerField(unique=True)
    cpn_code = models.CharField(max_length=3)
    cpn_name = models.CharField(max_length=100)
    ipo_market = models.CharField(max_length=10)

    def get_cpn_full_name(self):
        return self.cpn_code + " - " + self.cpn_name

    def __str__(self):
        return self.get_cpn_full_name()


class DataDetail(models.Model):
    cpn_id = models.IntegerField()
    date_record = models.DateField(unique=True)
    price = models.IntegerField()
