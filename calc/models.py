
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
class Bus(models.Model):
    from_data=models.CharField(max_length=200)
    to_data = models.CharField(max_length=200)

    busnumber=models.CharField(max_length=200)
    type=models.CharField(max_length=200)
    uid=models.IntegerField()
    ceats=models.IntegerField()
    cost=models.IntegerField(default=200)

    def __str__(self):
        return self.busnumber
class Stoppings(models.Model):
    stopping=models.CharField(max_length=200)
    b=models.ForeignKey(Bus,on_delete=models.CASCADE)

    def __str__(self):
        return self.stopping








# Create your models here.


class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)



def __str__(self):
    return self.from_data+"-"+self.to_data

