
from django.db import models
from django.conf import settings


class Building(models.Model):
    building_name = models.CharField(
        max_length=100,
        unique=True
    )

    building_code = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    latitude = models.DecimalField(
    max_digits=10,
    decimal_places=7,
    null=True,
    blank=True
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.building_name


class Room(models.Model):

    building = models.ForeignKey(
        Building,
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    room_number = models.CharField(
        max_length=20
    )

    floor_number = models.IntegerField(
    null=True,
    blank=True
    )

    point_id = models.IntegerField(
        null=True,
        blank=True
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['building', 'room_number'],
                name='unique_room_per_building'
            )
        ]

    def __str__(self):
        return f"{self.building.building_name} - {self.room_number}"

        
class Schedule(models.Model):

    class Day(models.TextChoices):
        MONDAY = "MON", "Monday"
        TUESDAY = "TUE", "Tuesday"
        WEDNESDAY = "WED", "Wednesday"
        THURSDAY = "THU", "Thursday"
        FRIDAY = "FRI", "Friday"
        SATURDAY = "SAT", "Saturday"
        SUNDAY = "SUN", "Sunday"

    class EntryMethod(models.TextChoices):
        MANUAL = "MANUAL", "Manual"
        AI = "AI", "AI Import"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schedules"
    )

    subject_name = models.CharField(max_length=100)
    subject_code = models.CharField(max_length=20)

    room = models.ForeignKey(
        Room, 
        on_delete=models.PROTECT,
        related_name='schedules')

    day_of_week = models.CharField(
        max_length=3,
        choices=Day.choices
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    entry_method = models.CharField(
        max_length=10,
        choices=EntryMethod.choices,
        default=EntryMethod.MANUAL
    )

    is_confirmed = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name}"