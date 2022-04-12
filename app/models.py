from distutils.command.upload import upload
from pydoc import describe
from djongo import models
from django.contrib.auth.models import User

# Create your models here.

class District(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Region(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Crop(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Year(models.Model):
    name = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)

class Visitor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joindate = models.DateField(auto_now_add=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    security_question = models.CharField(max_length=200)
    answer = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_username(self):
        return self.user.username

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joindate = models.DateField(auto_now_add=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_username(self):
        return self.user.username

class Officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joindate = models.DateField(auto_now_add=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=20)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    security_question = models.CharField(max_length=200)
    answer = models.CharField(max_length=100)
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_username(self):
        return self.user.username

class Soil(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class SoilLocationDetail(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    region = models.OneToOneField(Region, on_delete=models.CASCADE)
    soil = models.ForeignKey(Soil, on_delete=models.CASCADE)
    addon = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __self__(self):
        return self.id

class SoilDetail(models.Model):
    soil = models.OneToOneField(Soil, on_delete=models.CASCADE)
    detail = models.CharField(max_length=500)
    crop = models.CharField(max_length=250)

    def __self__(self):
        return self.id

class RainfallDetail(models.Model):
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    rainfall =models.FloatField()
    addon = models.DateField(auto_now_add=True)

    def __self__(self):
        return self.id

class CropDetail(models.Model):
    crop = models.OneToOneField(Crop, on_delete=models.CASCADE)
    soil = models.ForeignKey(Soil, on_delete=models.CASCADE)
    min_rainfall = models.FloatField(10)
    max_rainfall = models.FloatField(10)
    detail = models.CharField(max_length=500)
    status = models.BooleanField(default=False)

    def __self__(self):
        return self.id

class RequestSeed(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=500)
    crop = models.CharField(max_length=20)
    quantity = models.IntegerField(5)
    requeston = models.DateField(auto_now_add=True)
    approve = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)

    def __self__(self):
        return self.id

class RequestFertilizer(models.Model):
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    address = models.CharField(max_length=500)
    fertilizer = models.CharField(max_length=20)
    quantity = models.IntegerField(5)
    requeston = models.DateField(auto_now_add=True)
    approve = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)

    def __self__(self):
        return self.id

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joindate = models.DateField(auto_now_add=True)
    garden = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to='seller logo/')
    email = models.EmailField()
    describe = models.CharField(max_length=1000)
    address = models.CharField(max_length=500)
    gender = models.CharField(max_length=20)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    security_question = models.CharField(max_length=200)
    answer = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_username(self):
        return self.user.username