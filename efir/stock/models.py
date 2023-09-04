# Create your models here.
"""

class Stock(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, primary_key=True
    )  # product: This is a OneToOneField which means each Stock instance is linked to one Product instance. The on_delete parameter specifies what happens when the linked Product is deleted (in this case, the Stock will be deleted as well). The primary_key=True parameter indicates that the product field is the primary key of the Stock model.
    current_quantity = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"The quantity of {self.product} is now."
"""
