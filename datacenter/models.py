import django
from django.db import models

SECONDS_IN_HOUR = 3600
MINUTES_IN_HOUR = 60


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
    if time_exit:
        delta = time_exit - entry_time
    else:
        delta = time_now - entry_time

    return delta


def format_duration(duration):
    seconds_in_duration = duration.total_seconds()
    hours_in_duration = int(seconds_in_duration//SECONDS_IN_HOUR)
    minutes_in_duration = int((seconds_in_duration % SECONDS_IN_HOUR) // MINUTES_IN_HOUR)
    formated_duration = (f'{hours_in_duration}ч {minutes_in_duration}мин')

    return formated_duration


def is_visit_long(visit, minutes=60):
    second = visit.total_seconds()
    duration = int((second % SECONDS_IN_HOUR) // MINUTES_IN_HOUR)

    return duration > minutes
