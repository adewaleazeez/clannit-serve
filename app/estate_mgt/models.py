from django.db import models
from random import randint, shuffle
from django import forms


def estate_id():
    alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    for i in range(0,20):
        rand_int = randint(0, 9)
        alpha.append(str(rand_int))
    shuffle(alpha)
    return''.join(alpha[0:20])


class Estate(models.Model):
    estate_id = models.CharField(default=estate_id, primary_key=True, max_length=30)
    estate_name = models.CharField(max_length=200)
    estate_address = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.estate_name


class Street(models.Model):
    street_id = models.CharField(default=estate_id, primary_key=True, max_length=30)
    estate = models.ForeignKey(Estate, on_delete=models.CASCADE)
    street_name = models.CharField(max_length=250, unique=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.street_name


class Building(models.Model):
    building_id = models.CharField(default=estate_id, primary_key=True, max_length=30)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    building_number = models.CharField(max_length=250, unique=False)
    building_type = models.IntegerField(unique=False, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.building_number)


class Apartment(models.Model):
    apartment_id = models.CharField(default=estate_id, primary_key=True, max_length=30)
    street = models.ForeignKey(Street, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    apartment_number = models.CharField(max_length=250, unique=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Apartment: {} {} '.format(self.apartment_id, self.apartment_number)


class Salutation(models.Model):
    title_id = models.CharField(default=estate_id, primary_key=True, max_length=30)
    title_name = models.CharField(max_length=250, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title_name


class NewEstateForm(forms.ModelForm):
    class Meta:
        model = Estate
        fields = ['estate_id', 'estate_name', 'estate_address']
        widgets = {
            'estate_id': forms.TextInput(attrs={'class': 'form-control', }),
            'estate_name': forms.TextInput(attrs={'class': 'form-control', }),
            'estate_address': forms.TextInput(attrs={'class': 'form-control', })
        }


class NewStreetForm(forms.ModelForm):
    class Meta:
        model = Street
        fields = ['street_id', 'estate', 'street_name']
        widgets = {
            'street_id': forms.TextInput(attrs={'class': 'form-control', }),
            'estate': forms.Select(attrs={'class': 'form-control'}),
            'street_name': forms.TextInput(attrs={'class': 'form-control', })
        }


class NewBuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['building_id', 'street', 'building_number', 'building_type']
        widgets = {
            'building_id': forms.TextInput(attrs={'class': 'form-control', }),
            'street': forms.Select(attrs={'class': 'form-control'}),
            'building_number': forms.TextInput(attrs={'class': 'form-control', }),
            'building_type': forms.Select(attrs={'class': 'form-control'}),
        }


class NewApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['apartment_id', 'street', 'building', 'apartment_number']
        widgets = {
            'apartment_id': forms.TextInput(attrs={'class': 'form-control', }),
            'street': forms.Select(attrs={'class': 'form-control'}),
            'building': forms.Select(attrs={'class': 'form-control'}),
            'apartment_number': forms.TextInput(attrs={'class': 'form-control', })
        }


class NewSalutationForm(forms.ModelForm):
    class Meta:
        model = Salutation
        fields = ['title_id', 'title_name']
        widgets = {
            'title_id': forms.TextInput(attrs={'class': 'form-control', }),
            'title_name': forms.TextInput(attrs={'class': 'form-control', })
        }


