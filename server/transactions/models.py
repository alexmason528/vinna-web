from django.db import models

# Create your models here.


class Transaction(models.Model):
  
  transaction_id = models.CharField(max_length=36) # TODO Shard
  date = models.DateTimeField('Transaction Date')
  amount = models.DecimalField(decimal_places=2, max_digits=9)


  def __str__(self):
    return self.text