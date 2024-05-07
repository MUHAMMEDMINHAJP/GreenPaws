from django.db import models

# Create your models here.
class Login(models.Model):
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)
    logintype=models.CharField(max_length=30)

class Shop(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    shop_name=models.CharField(max_length=30)
    owner_name=models.CharField(max_length=30)
    email=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    post=models.CharField(max_length=30)
    pin=models.IntegerField()
    photo=models.CharField(max_length=300)
    licence=models.CharField(max_length=300)
    shop_type=models.CharField(max_length=30)
    district=models.CharField(max_length=30,default=0)
    status=models.CharField(max_length=30)
    ph_no=models.BigIntegerField()

class User(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    ph_no=models.BigIntegerField()
    email=models.CharField(max_length=30)
    gender = models.CharField(max_length=30,default="")
    dob=models.DateField()
    place=models.CharField(max_length=30)
    post=models.CharField(max_length=30)
    pin=models.IntegerField()
    district = models.CharField(max_length=30,default=0)

class Delivery_boy (models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    ph_no = models.BigIntegerField()
    email=models.CharField(max_length=30)
    place = models.CharField(max_length=30)
    post=models.CharField(max_length=30)
    pin=models.IntegerField()
    photo = models.CharField(max_length=300)
    id_proof=models.CharField(max_length=300)
    gender=models.CharField(max_length=300)

class Plant (models.Model):
    SHOP_ID=models.ForeignKey(Shop,on_delete=models.CASCADE)
    plant_name=models.CharField(max_length=30)
    scientific_name=models.CharField(max_length=30)
    size=models.CharField(max_length=30)
    plant_type=models.CharField(max_length=30)
    photo=models.CharField(max_length=300)
    price=models.CharField(max_length=30)
    details=models.CharField(max_length=5000)


class Plant_stock(models.Model):
    PLANT= models.ForeignKey(Plant, on_delete=models.CASCADE)
    stock= models.IntegerField()

class Plant_cart(models.Model):
    PLANT=models.ForeignKey(Plant, on_delete=models.CASCADE)
    USER=models.ForeignKey(User, on_delete=models.CASCADE)
    quantity=models.CharField(max_length=30)

class Pet (models.Model):
    SHOP_ID=models.ForeignKey(Shop,on_delete=models.CASCADE)
    pet_name=models.CharField(max_length=30)
    breed_name=models.CharField(max_length=30)
    photo=models.CharField(max_length=300)
    age=models.CharField(max_length=30)
    # pet_type=models.CharField(max_length=30)
    price=models.CharField(max_length=30)
    details=models.CharField(max_length=1000)

class Pet_stock (models.Model):
    PET= models.ForeignKey(Pet, on_delete=models.CASCADE)
    stock= models.CharField(max_length=30)


class Pet_cart(models.Model):
    PET = models.ForeignKey(Pet, on_delete=models.CASCADE)
    USER = models.ForeignKey(User, on_delete=models.CASCADE,default='')
    quantity = models.CharField(max_length=30)


# class User(models.Model):
#     LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
#     name=models.CharField(max_length=30)
#     ph_no = models.BigIntegerField()
#     email=models.CharField(max_length=30)
#     place=models.CharField(max_length=30)
#     post=models.CharField(max_length=30)
#     pin=models.IntegerField()
#     gender=models.CharField(max_length=30)
#     district=models.CharField(max_length=30)

class DeliveryBoy(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    ph_no = models.BigIntegerField()
    email=models.CharField(max_length=30)
    place=models.CharField(max_length=30)
    post=models.CharField(max_length=30)
    pin=models.IntegerField()
    gender=models.CharField(max_length=30)
    district=models.CharField(max_length=30)
    photo = models.CharField(max_length=300)
    idproof = models.CharField(max_length=300)
    latitude=models.CharField(max_length=300)
    longitude=models.CharField(max_length=300)
    status = models.CharField(max_length=30,default='')

class DeliveryAddress(models.Model):
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    ph_no = models.BigIntegerField()
    place = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    post = models.CharField(max_length=30)
    pin = models.IntegerField()
    landmark = models.CharField(max_length=30)
    district = models.CharField(max_length=30, default=0)



class Plant_ordermain(models.Model):
    SHOP= models.ForeignKey(Shop, on_delete=models.CASCADE)
    date=models.DateField()
    deldate=models.CharField(max_length=100,default='')
    amount=models.CharField(max_length=100,default='')
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    ADDRESS=models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE)
    status=models.CharField(max_length=30)


class Plant_ordersub(models.Model):
    PLANT_ORDERMAIN= models.ForeignKey(Plant_ordermain, on_delete=models.CASCADE)
    PLANT = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=30)

class Pet_ordermain(models.Model):
    SHOP= models.ForeignKey(Shop, on_delete=models.CASCADE)
    date=models.DateField()
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    ADDRESS=models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE)
    status=models.CharField(max_length=30)



class Pet_ordersub(models.Model):
    PET_ORDERMAIN= models.ForeignKey(Pet_ordermain, on_delete=models.CASCADE)
    PET = models.ForeignKey(Pet, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=30)



class Payment(models.Model):
    PLANT_ORDERMAIN= models.ForeignKey(Plant_ordermain, on_delete=models.CASCADE)

class Assigned_order(models.Model):
    DELIVERY= models.ForeignKey(DeliveryBoy, on_delete=models.CASCADE)
    ORDERMAIN= models.ForeignKey(Plant_ordermain, on_delete=models.CASCADE)
    status= models.CharField(max_length=30)
    date= models.DateField()

class Plantreview(models.Model):
    SHOP= models.ForeignKey(Shop, on_delete=models.CASCADE)
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    review = models.CharField(max_length=300)
    rating = models.CharField(max_length=300)

