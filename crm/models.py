from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
class Client(models.Model):
    name=models.CharField(max_length=255)
    company=models.CharField(max_length=250)
    email=models.EmailField()
    phone=models.CharField(max_length=15)
    address=models.TextField()
    date_added=models.DateField(auto_now_add=True,null=True,blank=True)
    added_by=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)


    def __str__(self):
        return f"{self.name} {self.company} added by {self.added_by}"

class Product(models.Model):
    product_name=models.CharField(max_length=150)
    cost_price=models.DecimalField(max_digits=10,decimal_places=2)
    product_qty=models.IntegerField()
    previous_qty = models.IntegerField(default=0)
    added_by=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    def total_price(self):
        return self.cost_price * self.product_qty

    def __str__(self):
        return f"{self.product_name} qty:{self.product_qty}"
    
    def save(self, *args, **kwargs):
        # If the product is already saved in the database (has an ID), store the current quantity in `previous_qty`
        if self.pk:
            # Get the existing product object from the database
            existing_product = Product.objects.get(pk=self.pk)
            self.previous_qty = existing_product.product_qty  
        super().save(*args, **kwargs)
    
    def reduce_stock(self, qty):
        if self.product_qty >= qty:
            self.product_qty -= qty
            self.save()  # Save the updated stock to the database
        else:
            raise ValueError("Insufficient stock available")



class Opportunity(models.Model):
    STATUS_CHOICES=[('Open','Open'),
                    ('Won','Won'),
                    ('Lost','Lost'),
                    ]
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    opportunity_name=models.CharField(max_length=255)
    estimated_value=models.DecimalField(max_digits=10,decimal_places=2)
    requirement=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='requirements')
    estimated_qty=models.IntegerField()
    status=models.CharField(max_length=10,choices=STATUS_CHOICES)
    added_by=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    date_added=models.DateField(auto_now_add=True,null=True,blank=True)


    def __str__(self):
        return f"{self.opportunity_name} - {self.client.name}"
    
    # def save(self, *args, **kwargs):
    #     # Check if the product stock is sufficient before saving the shipping receipt
    #     if self.requirement:
    #         self.requirement.reduce_stock(self.estimated_qty)  # Reduce the stock of the product
        
    #     # Save the shipping receipt after adjusting the stock
    #     super(Opportunity, self).save(*args, **kwargs)

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)  # Link to Opportunity
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True,blank=True)  # Link to a product
    quantity = models.PositiveIntegerField(default=1)
    date = models.DateField(auto_now_add=True)  # Automatically set the date of the invoice
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)  # Add optional payment date
    payment_method = models.CharField(max_length=50, choices=[('Credit', 'Credit'), ('Cash', 'Cash'), ('Transfer', 'Online Transfer')], null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')])
    added_by=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    TAX_RATE = Decimal('0.18')
    def save(self, *args, **kwargs):
        """Override save method to calculate total amount before saving."""
        if self.product and self.quantity:
            self.total_amount = self.product.cost_price * self.quantity  # Set total_amount based on product price and quantity
        super().save(*args, **kwargs)

    def product_tax(self):
        """Calculate tax based on total_amount."""
        return self.total_amount * self.TAX_RATE

    def total_with_tax(self):
        """Calculate total amount including tax."""
        return self.total_amount + self.product_tax()

    def __str__(self):
        return f"Invoice #{self.id} - {self.client.name} - {self.total_amount}"
    

class Shipping_Receipt(models.Model):
    DELIVERY_STATUS=[('pending','Pending'),
                     ('dispatch','Dispatch'),
                     ('delivered','Delivered'),
                     ]
    client=models.ForeignKey(Client,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add='True')
    delivery_address=models.CharField(max_length=255)
    delivery_status = models.CharField(max_length=10, choices=DELIVERY_STATUS, default='pending')
    date_added=models.DateField(auto_now_add=True,null=True,blank=True) 
    added_by=models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, null=True, blank=True)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)  # Quantity being shipped


    def __str__(self):
        return f"Shipping receipt for {self.client} - {self.delivery_status}"
    
    def save(self, *args, **kwargs):
        # Check if the product stock is sufficient before saving the shipping receipt
        if self.product:
            self.product.reduce_stock(self.quantity)  # Reduce the stock of the product
        
        # Save the shipping receipt after adjusting the stock
        super(Shipping_Receipt, self).save(*args, **kwargs)

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    # Link UserProfile to a User
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Existing fields
    department = models.CharField(max_length=100, choices=[
        ('Accounts', 'Accounts'),
        ('HR', 'HR'),
        ('Sales', 'Sales'),
        ('Inventory', 'Inventory'),
        ('Tech', 'Tech'),
    ])
    phone = models.CharField(max_length=15, blank=True, null=True)

    role=models.CharField(max_length=100,choices=[
        ('Regional Accounts manager','Regional Accounts manager'),
        ('Regional Sales Manager','Regional Sales Manager'),
        ('Chief Technical Officer','Chief Technical Officer'),
        ('Regional SCM manager','Regional SCM manager'),
        ('Sales Executive', 'Sales Executive'),
        ('Accounts Executive', 'Accounts Executive'),
        ('HR Executive', 'HR Executive'),
        ('IT Engineer', 'IT Engineer'),
        ('SCM Executive', 'SCM Executive'),
    ],default='Regional Sales Manager')

    # New fields for gender and age
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.department}"

