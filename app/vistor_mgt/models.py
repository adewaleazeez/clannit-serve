from django.db import models
from app.user.models import User
from app.estate_mgt.models import Estate
from random import shuffle,randint
from utliz.mobile_number_formater import mobile_number
from utliz.send_sms import send_sms
# Create your models here.


def unique_code():
    alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    for i in range(0,100):
        rand_int = randint(0, 9)
        alpha.append(str(rand_int))
    shuffle(alpha)
    return''.join(alpha[0:5])


class NewVistor(models.Model):
    vistor_first_name = models.CharField(max_length=120, null=True)
    vistor_last_name = models.CharField(max_length=120, null=True)
    vistor_mobile_number = models.BigIntegerField()
    whom_to_see = models.ForeignKey(User, on_delete=models.CASCADE)
    vistor_unique_code = models.CharField(default=unique_code, max_length=6)
    unique_code_is_active = models.BooleanField(default=True)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    checked_in = models.BooleanField(default=False)
    checked_out = models.BooleanField(default=False)
    checked_in_date = models.DateTimeField(auto_now_add=False,blank=True, null=True)
    checked_out_date = models.DateTimeField(auto_now_add=False,blank=True, null=True)

    def save(self,*args, **kwargs):
        if not self.pk:
            self.vistor_mobile_number = mobile_number(str(self.vistor_mobile_number))
            #Send Sms to Visitor
            message = 'HI {} you have been invited by {} to {}. Please find' \
                      ' your Unique Entry Code {} as this is to be requested' \
                      ' for at the gate. '.format(self.vistor_first_name,self.whom_to_see.first_name,
                                                 self.whom_to_see.estate,self.vistor_unique_code)
            number = self.vistor_mobile_number
            send_sms(number,message)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.vistor_first_name
