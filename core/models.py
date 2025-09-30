from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Custom User model with roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('adminx', 'AdminX'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.username} ({self.role})"

# Clients or Projects
class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Categories like “ON MODEL”
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Pricing per category
class Pricing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_type = models.CharField(max_length=50)  # e.g., "default", "4-5 SIZING"
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.category.name} ({self.price_type}) - ${self.price}"

# Work logs from users
class WorkLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price_type = models.CharField(max_length=50, blank=True)
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    submitted_at = models.DateTimeField(auto_now_add=True)

# Invoices (auto-generated XLS)
class Invoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    file_url = models.CharField(max_length=255)  # Path to the XLS
    created_at = models.DateTimeField(auto_now_add=True)

# Logs of who did what
class UserLoginHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    login_datetime = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_type = models.CharField(max_length=50)
    browser = models.CharField(max_length=50)
    os = models.CharField(max_length=50)

    class Meta:
        ordering = ['-login_datetime']

    def __str__(self):
        return f"{self.user.username} - {self.login_datetime}"

class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action_by = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)