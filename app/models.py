from django.core.validators import MaxValueValidator, MinValueValidator
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
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)
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
    organic_carbon = models.FloatField()
    phosphorous = models.FloatField()
    potassium = models.FloatField()
    manganese = models.FloatField()
    sulphur = models.FloatField()
    ph_value = models.FloatField()
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
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user.id)
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_username(self):
        return self.user.username

class Product(models.Model):
    product_name = models.CharField(max_length=30)
    describe = models.CharField(max_length=1000)
    joindate = models.DateField(auto_now_add=True)
    image_1 = models.ImageField(upload_to='product image/')
    image_2 = models.ImageField(upload_to='product image/')
    image_3 = models.ImageField(upload_to='product image/')
    image_4 = models.ImageField(upload_to='product image/')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.CharField(max_length=30)
    price = models.IntegerField()
    price_per_quantity = models.CharField(max_length=20)
    status = models.BooleanField(default=False)
    stock = models.BooleanField(default=True)
    activity = models.BooleanField(default=True)

    def __self__(self):
        return self.id

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(1)])
    address = models.CharField(max_length=500)
    shipped = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    order = models.BooleanField(default=True)
    payment=models.BooleanField(default=False)
    order_on = models.DateField(auto_now_add=True)

    def __self__(self):
        return self.id

    @property
    def get_garden(self):
        return self.product.seller.garden

class Pay(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    card_number = models.CharField(max_length=20)
    month = models.IntegerField()
    year = models.IntegerField()
    cvv_number = models.IntegerField()
    amount = models.IntegerField()
    payment_on = models.DateField(auto_now_add=True)

    def __self__(self):
        return self.id