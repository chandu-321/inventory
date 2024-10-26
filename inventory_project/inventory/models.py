from django.db import models

class Inventory(models.Model):
    # Fields
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # This will automatically become the primary key if none is specified.
    def __str__(self):
        return self.name