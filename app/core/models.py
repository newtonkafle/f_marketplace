from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.utils import send_notification


class UserManger(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, phone_number, password=None):
        if not email:
            raise ValueError('User must have an email')
        if not username:
            raise ValueError('User must have username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True

        user.save(using=self._db)

        return user

# ------ User -----#


class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2

    ROLE_CHOICE = (
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    role = models.PositiveIntegerField(
        choices=ROLE_CHOICE, blank=True, null=True)

    # required fields
    date_joined = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManger()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


# ------User Profile------#

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='core/profile_pictures', blank=True, null=True)
    cover_picture = models.ImageField(
        upload_to='core/cover_pictures', blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    state = models.CharField(max_length=20, blank=True, null=True)
    post_code = models.CharField(max_length=10, blank=True, null=True)
    longitude = models.CharField(max_length=30, blank=True, null=True)
    latitude = models.CharField(max_length=30, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True)

    def full_address(self):
        return f'{self.address}, {self.state}, {self.country}, {self.post_code}'

    def __str__(self):
        return self.user.email

# ------ Vendor --------#


class Vendor(models.Model):
    user = models.OneToOneField(
        User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(
        UserProfile, related_name='user_profile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vendor_name

    def save(self, *args, **kwargs):
        """ overriding the save function of the django."""
        if self.pk is not None:
            db_vendor = Vendor.objects.get(pk=self.pk)
            if db_vendor.is_approved != self.is_approved:
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                }
                print(context['is_approved'])
                send_notification('VA', context)

        return super(Vendor, self).save(*args, **kwargs)


# ------- Vendor Menu Models------#


# ----- product category model ---#
class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def clean(self):
        name_words = [word.capitalize()
                      for word in self.category_name.split(' ')]

        self.category_name = " ".join(name_words)
        print(self.category_name)

    def __str__(self):
        return self.category_name


# ----- product model ----#

class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    product_title = models.CharField(unique=True, max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='vendor/foodimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_title

    def clean(self):
        name_words = [word.capitalize()
                      for word in self.product_title.split(' ')]

        self.product_title = " ".join(name_words)
        print(self.product_title)


# --------- cart model -------#

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user
