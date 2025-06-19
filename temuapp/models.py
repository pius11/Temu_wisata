from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    no_hp = models.CharField(max_length=14, unique=True, null=True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    foto_profile = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # Ubah ke ImageField
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('regular', 'Regular User')], default='regular')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    @property
    def id(self):
        return self.user_id

    class Meta:
        db_table = 'users'


class TouristSpot(models.Model):
    spot_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    kota = models.TextField()
    kecamatan = models.TextField()
    desa = models.TextField()
    fasilitas = models.TextField()
    google_maps_url = models.URLField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_spots')
    price_min = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    price_max = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)  # <--- Tambah
    is_removed = models.BooleanField(default=False)   # <--- Tambah
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tourist_spots'

class SpotImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    spot_id = models.ForeignKey(TouristSpot, on_delete=models.CASCADE, related_name='images')
    file_name = models.ImageField(upload_to='spot_images/')  # Ubah dari CharField ke ImageField
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'spot_images'

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    spot_id = models.ForeignKey(TouristSpot, on_delete=models.CASCADE, related_name='reviews')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    review_text = models.TextField(null=True, blank=True)
    is_reported = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reviews'
        constraints = [
            models.CheckConstraint(
                check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                name='rating_range'
            ),
        ]

class ReviewImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='images')
    file_name = models.ImageField(upload_to='review_images/')  # Ubah dari CharField ke ImageField
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_images'

# class ChatSession(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Session {self.id} - {self.user.username}"

# class ChatMessage(models.Model):
#     session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
#     sender = models.CharField(max_length=10, choices=[('user', 'User'), ('ai', 'AI')])
#     message = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.sender} at {self.created_at}"

class FavoriteSpot(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_spots')
    spot = models.ForeignKey(TouristSpot, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favorite_spots'
        unique_together = ('user', 'spot')  # Satu user tidak bisa menyimpan spot yang sama dua kali