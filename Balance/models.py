from django.db import models


# Create your models here.
class Category(models.Model):
    Category = models.CharField(max_length=255)


class Product(models.Model):
    Product = models.CharField(max_length=255)


class Store(models.Model):
    Store = models.CharField(max_length=255)


class Transaction(models.Model):
    Timestamp = models.DateTimeField()
    Amount = models.FloatField()
    Banknumber = models.CharField(max_length=255)
    Description = models.CharField(max_length=255)
    Category = models.ForeignKey(Category)
    Store = models.ForeignKey(Store)


class Rule(models.Model):
    Name = models.CharField(max_length=255)
    Find = models.CharField(max_length=255)
    Replace = models.CharField(max_length=255)
    Tags = models.CharField(max_length=255)
