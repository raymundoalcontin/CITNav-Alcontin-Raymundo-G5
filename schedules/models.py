
from django.db import models
from django.conf import settings


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

    room = models.CharField(max_length=50)
    building = models.CharField(max_length=100)

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
