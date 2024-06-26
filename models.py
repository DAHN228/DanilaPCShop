from django.db import models


class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=512)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'customers'


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=512)
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'
