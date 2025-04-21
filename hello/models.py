from django.db import models

# Create your models here.
class Membership(models.Model):
    user_id = models.IntegerField()
    club_id = models.IntegerField()
    def __str__(self):
        return self.user_id
    class Meta:
        db_table="Membership"

class Users(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    user_id = models.AutoField(primary_key=True);
    interest_level =models.CharField(max_length=255)
    def __str__(self):
        return self.name
    class Meta:
          db_table="Users"    
class Club(models.Model):
    name = models.CharField(max_length=255)
    num_courts = models.IntegerField()
    club_id = models.AutoField(primary_key=True)
    def __str__(self):
        return self.name
    class Meta:
        db_table="Club"
