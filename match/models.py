from django.db import models

class UserMatch(models.Model):

    date_difference = models.IntegerField()
    is_retired      = models.BooleanField(default =False)
    track_name      = models.CharField(max_length = 100)
    kart_name       = models.CharField(max_length = 50)
    lap_time        = models.CharField(max_length = 50)
    match_id_list   = models.TextField()
    game_user       = models.OneToOneField("rank.GameUsers", on_delete = models.CASCADE)

    class Meta:
        db_table    = "user_matches"
