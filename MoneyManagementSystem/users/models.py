from django.db import models

# Create your models here.
class Users(models.Model):
    name=models.CharField(max_length=120)
    address=models.CharField(max_length=150)
    email=models.CharField(max_length=150,unique=True)
    phone=models.CharField(max_length=12)
    username=models.CharField(max_length=120,unique=True)
    password=models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Category(models.Model):
    category_name=models.CharField(max_length=150,unique=True)

    def __str__(self):
        return self.category_name


class Expense(models.Model):
    user=models.CharField(max_length=120)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    amount=models.IntegerField()
    shortnote=models.CharField(max_length=250)
    date=models.DateField()

    def __str__(self):
        return str(self.amount)

