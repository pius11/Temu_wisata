from django.db import models


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password_hash = models.CharField(max_length=255)
    no_hp = models.CharField(max_length=14, unique=True, null= True, blank=True)
    alamat = models.TextField(null=True, blank=True)
    foto_profile = models.TextField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('regular', 'Regular User')], default='regular')
    created_at = models.DateTimeField(auto_now_add=True)

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
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_verified = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)  # <--- Tambah
    is_removed = models.BooleanField(default=False)   # <--- Tambah
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tourist_spots'

class SpotImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    spot_id = models.ForeignKey(TouristSpot, on_delete=models.CASCADE, related_name='images')
    file_name = models.CharField(max_length=255)
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
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review_images'

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE)
    reporter_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports_made')
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')
    admin_action = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'reports'

class ReportTouristSpot(models.Model):
    report_id = models.AutoField(primary_key=True)
    spot_id = models.ForeignKey(TouristSpot, on_delete=models.CASCADE, related_name='reports')
    reporter_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spot_reports_made')
    reason = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')
    admin_action = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'report_tourist_spots'