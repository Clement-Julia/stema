from django.db import models

# Create your models here.
class Mod(models.Model):
    name = models.CharField(max_length=255)
    summary = models.TextField()
    description = models.TextField()
    picture_url = models.CharField(max_length=255)
    mod_downloads = models.IntegerField()
    mod_unique_downloads = models.IntegerField()
    uui = models.CharField(max_length=255)
    mod_id = models.IntegerField()
    game_id = models.IntegerField()
    domain_name = models.CharField(max_length=255)
    category_id = models.IntegerField()
    created_timestamp = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_timestamp = models.IntegerField()
    updated_time = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=255)
    uploaded_by = models.CharField(max_length=255)
    uploaded_users_profile_url = models.CharField(max_length=255)
    contains_adult_content = models.BooleanField()
    status = models.CharField(max_length=255)
    available = models.BooleanField()


    def __str__(self):
        return self.name