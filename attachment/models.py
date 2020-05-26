from django.db import models
from django.conf import settings
# Create your models here.
class Rates(models.Model):
    date = models.DateField()
    EUR = models.IntegerField()
    USD = models.IntegerField()
    JPY = models.IntegerField()
    CNY = models.IntegerField()
    EUR_n = models.IntegerField()
    USD_n = models.IntegerField()
    JPY_n = models.IntegerField()
    CNY_n = models.IntegerField()

    def insert(self):
        print(self.date)
        return "INSERT INTO `db`.`table` (`DATE`, `EUR`, `USD`, `JPY`, `CNY`, `EUR_n`, `USD_n`, `JPY_n`, `CNY_n`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" %(
            self.date, self.EUR, self.USD, self.JPY, self.CNY, self.EUR_n, self.USD_n, self.JPY_n, self.CNY_n)