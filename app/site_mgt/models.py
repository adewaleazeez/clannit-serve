from django.db import models

# Create your models here.


def upload_path(instance, filename):
    return instance.get_upload_path(filename)


class EstateDetail(models.Model):
    estate_name = models.CharField(max_length=300, default='SERVE ESTATE')
    estate_address = models.CharField(max_length=500, default='14a, sasegbon Ikeja GRA')
    estate_logo = models.ImageField(upload_to=upload_path, blank=True, null=True)

    def __str__(self):
        return self.estate_name

    def get_upload_path(self,filename):
        return "estate_image/{}".format(filename)

    class Meta:
        verbose_name = 'Estate Detail'
        verbose_name_plural = 'Estate Detail'