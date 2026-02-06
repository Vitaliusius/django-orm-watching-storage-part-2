from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from .models import get_duration, format_duration, is_visit_long
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    worker_in_passcard = get_object_or_404(Passcard, passcode=passcode)
    worker_in_visit = Visit.objects.filter(passcard=worker_in_passcard)
    this_passcard_visits = []
    for visit in worker_in_visit:
        parameters_visit_long = {
            'entered_at': visit.entered_at,
            'duration': format_duration(get_duration(visit.entered_at, visit.leaved_at)),
            'is_strange': is_visit_long(get_duration(visit.entered_at, visit.leaved_at))
        }
        this_passcard_visits.append(parameters_visit_long)

    context = {
        'passcard': worker_in_passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
