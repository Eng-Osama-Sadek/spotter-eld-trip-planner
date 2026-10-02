from django.db import models


class FuelStation(models.Model):
    opis_truckstop_id = models.IntegerField(db_index=True)
    truckstop_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=8)
    rack_id = models.IntegerField(null=True, blank=True)
    retail_price = models.FloatField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["retail_price"]

    def __str__(self):
        return f"{self.truckstop_name} - {self.city}, {self.state}"
