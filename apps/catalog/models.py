from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available_sizes = models.JSONField(default=list, blank=True) # e.g. ["XS", "S", "M"]
    is_active = models.BooleanField(default=True)

    # Detailed Characteristics
    collection = models.CharField(max_length=255, blank=True, null=True)
    frame_material = models.CharField(max_length=255, blank=True, null=True)  # e.g. "Silver Metal Frame"
    lens_type = models.CharField(max_length=255, blank=True, null=True)      # e.g. "Clear Lenses"
    shape = models.CharField(max_length=100, blank=True, null=True)          # e.g. "Square Shape"
    uv_protection = models.CharField(max_length=255, blank=True, null=True)  # e.g. "99.9% of UV Rays"
    
    # Dimensions (in mm)
    lens_width = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    bridge_width = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    frame_front_width = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    temple_length = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    lens_height = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    
    country_of_origin = models.CharField(max_length=100, blank=True, null=True) # e.g. "China"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"
