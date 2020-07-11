from django.db import models

class GameUser(models.Model):

    access_id = models.CharField(max_length = 50)
    nickname  = models.CharField(max_length = 50)

    class Meta:
        db_table = "game_users"

    def __str__(self):
        return self.access_id

class UserPageHit(models.Model):

    count     = models.IntegerField()
    game_user = models.OneToOneField("GameUser", on_delete = models.CASCADE, null = True)

    class Meta:
        db_table = "user_page_hits"

    def __str__(self):
        return self.count

class Comment(models.Model):

    comment = models.TextField()
    from_id = models.ForeignKey("GameUser", on_delete = models.CASCADE, related_name = "to_id")
    to_id   = models.ForeignKey("GameUser", on_delete = models.CASCADE, related_name = "from_id")

    class Meta:
        db_table = "comments"

    def __str__(self):
        return self.comment

class UserTrackRecord(models.Model):

    cumul_dist = models.TextField()
    game_user  = models.ForeignKey("GameUser", on_delete = models.CASCADE)
    track      = models.ForeignKey("metadata.Track", on_delete = models.CASCADE)

    class Meta:
        db_table = "user_track_records"

class UserTrackInfo(models.Model):

    play_cnt   = models.IntegerField()
    win_ratio  = models.IntegerField()
    best_lap   = models.CharField(max_length = 50)
    game_user  = models.OneToOneField("GameUser", on_delete = models.CASCADE)
    track      = models.OneToOneField("metadata.Track", on_delete = models.CASCADE)

    class Meta:
        db_table = "user_track_info"

class UserKart(models.Model):

    play_cnt      = models.IntegerField()
    win_ratio     = models.IntegerField()
    retire_ratio  = models.IntegerField()
    track_history = models.TextField()
    game_user     = models.OneToOneField("GameUser", on_delete = models.CASCADE)
    kart          = models.OneToOneField("metadata.Kart", on_delete = models.CASCADE)

    class Meta:
        db_table = "user_kart"

class SpeedType(models.Model):

    name = models.CharField(max_length = 50)

    class Meta:
        db_table = "speed_types"

    def __str__(self):
        return self.name

class TeamType(models.Model):

    name = models.CharField(max_length = 50)

    class Meta:
        db_table = "team_types"

    def __str__(self):
        return self.name

class Detail(models.Model):

    play_cnt       = models.IntegerField()
    win_cnt        = models.IntegerField()
    retire_pct     = models.DecimalField(max_digits = 10, decimal_places = 2)
    rank_avg_50    = models.DecimalField(max_digits = 10, decimal_places = 2)
    rank_avg_500   = models.DecimalField(max_digits = 10, decimal_places = 2)
    rank_list_50   = models.CharField(max_length = 300)
    expected_ratio = models.DecimalField(max_digits = 10, decimal_places = 2)
    game_user      = models.OneToOneField("GameUser", on_delete = models.CASCADE)
    character      = models.ForeignKey("metadata.Character", on_delete = models.SET_NULL, null = True)
    team_type      = models.ForeignKey("TeamType", on_delete = models.SET_NULL, null = True)
    speed_type     = models.ForeignKey("SpeedType", on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = "details"

class Ranking(models.Model):

    rank        = models.IntegerField()
    rank_diff   = models.IntegerField()
    cumul_point = models.IntegerField()
    point_get   = models.IntegerField()
    win_pct     = models.DecimalField(max_digits = 10, decimal_places = 2)
    retire_pct  = models.DecimalField(max_digits = 10, decimal_places = 2)
    play_cnt    = models.IntegerField()
    avg_rank    = models.IntegerField()
    game_user   = models.OneToOneField("GameUser", on_delete = models.CASCADE)
    speed_type  = models.ForeignKey("SpeedType", on_delete = models.SET_NULL, null = True)
    team_type   = models.ForeignKey("TeamType", on_delete = models.SET_NULL, null = True)

    class Meta:
        db_table = "rankings"
