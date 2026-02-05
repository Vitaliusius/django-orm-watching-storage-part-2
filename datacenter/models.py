import django
from django.db import models


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(entry_time, time_exit):
    time_now = django.utils.timezone.localtime()
    if time_exit == None:
        delta = time_now - entry_time
    else:
        delta = time_exit - entry_time

    return delta


def format_duration(duration):
    seconds_in_duration = duration.total_seconds()
    seconds_in_hour = 3600
    minutes_in_hour = 60
    hours_in_duration = int(seconds_in_duration//seconds_in_hour)
    minutes_in_duration = int((seconds_in_duration % seconds_in_hour) // minutes_in_hour)
    formated_duration = (f'{hours_in_duration}ч {minutes_in_duration}мин')
    
    return formated_duration


def is_visit_long(visit, minutes=60):
    second = visit.total_seconds()
    seconds_in_hour = 3600
    minutes_in_hour = 60
    duration = int((second % seconds_in_hour) // minutes_in_hour)
    
    return duration < minutes
     