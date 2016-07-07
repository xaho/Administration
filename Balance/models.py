from django.db import models


# Create your models here.
class Category(models.Model):
    Category = models.CharField(max_length=255)


class Product(models.Model):
    Product = models.CharField(max_length=255)


class Store(models.Model):
    Store = models.CharField(max_length=255)


class Transaction(models.Model):
    Date = models.DateField()
    Amount = models.FloatField()
    Destination = models.CharField(max_length=255)
    Description = models.CharField(max_length=1023)
    Category = models.ForeignKey(Category, null=True)
    Store = models.ForeignKey(Store, null=True)
    Processed = models.BooleanField()


class Rule(models.Model):
    Name = models.CharField(max_length=255)
    Find = models.CharField(max_length=255)
    Replace = models.CharField(max_length=255)
    Tags = models.CharField(max_length=255)
