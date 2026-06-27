from django.db import models
from django.utils import timezone


class Company(models.Model):
    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'verification'

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('seed', 'Seed'),
        ('fertilizer', 'Fertilizer'),
        ('pesticide', 'Pesticide'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    barcode = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'verification'

    def __str__(self):
        return self.name


class Batch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch_number = models.CharField(max_length=100, unique=True)
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'verification'

    def __str__(self):
        return self.batch_number

    def is_expired(self):
        return timezone.now().date() > self.expiry_date


class Verification(models.Model):
    RESULT_CHOICES = [
        ('asli', 'Asli'),
        ('nakli', 'Nakli'),
        ('expired', 'Expired'),
    ]
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True)
    barcode_scanned = models.CharField(max_length=200)
    result = models.CharField(max_length=20, choices=RESULT_CHOICES)
    location = models.CharField(max_length=200, blank=True)
    scanned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'verification'

    def __str__(self):
        return f"{self.barcode_scanned} - {self.result}"