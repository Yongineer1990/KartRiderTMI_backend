from django.db import models

class Users(models.Model):

    kakao_id  = models.CharField(max_length = 50, null = True)
    email     = models.EmailField(max_length = 200)
    picture   = models.URLField()
    game_user = models.OneToOneField("rank.GameUser", on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.kakao_id
