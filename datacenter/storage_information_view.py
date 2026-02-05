from datacenter.models import Visit
from django.shortcuts import render
from .models import get_duration, format_duration


def storage_information_view(request):
    people_inside = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = []
    for worker in people_inside:
        duration = get_duration(worker.entered_at, worker.leaved_at)
        worker_duration_visit = {
            'who_entered': worker.passcard,
            'entered_at':  worker.entered_at,
            'duration': format_duration(duration),
            }
        non_closed_visits.append(worker_duration_visit)
    context = {
        'non_closed_visits': non_closed_visits, 
    }
    return render(request, 'storage_information.html', context)
