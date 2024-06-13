from django.db import models
from django.contrib.auth.models import User

class GameLibrary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game_id = models.CharField(max_length=100)
    game_name = models.CharField(max_length=255)

    class Meta:
        unique_together = ('user', 'game_id')

    def __str__(self):
        return f"{self.user.username} - {self.game_name}"
