from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.shortcuts import redirect, render

from .models import Building, Room, Schedule


@login_required
def schedule_list(request):
    schedules = Schedule.objects.filter(
        user=request.user
    ).order_by('day_of_week', 'start_time')

    return render(
        request,
        'schedules/schedules_list.html',
        {'schedules': schedules}
    )


@login_required
def create_schedule(request):
    if request.method == 'POST':
        subject_names = request.POST.getlist('subject_name')
        subject_codes = request.POST.getlist('subject_code')
        room_ids = request.POST.getlist('room')
        building_ids = request.POST.getlist('building')
        days = request.POST.getlist('day_of_week')
        start_times = request.POST.getlist('start_time')
        end_times = request.POST.getlist('end_time')

        field_lists = [
            subject_names,
            subject_codes,
            room_ids,
            building_ids,
            days,
            start_times,
            end_times,
        ]

        try:
            if not subject_names or any(
                len(field) != len(subject_names) for field in field_lists
            ):
                raise ValueError("Please complete all schedule fields.")

            new_schedules = []

            for i in range(len(subject_names)):
                if not all([
                    subject_names[i].strip(),
                    subject_codes[i].strip(),
                    room_ids[i],
                    building_ids[i],
                    days[i],
                    start_times[i],
                    end_times[i],
                ]):
                    raise ValueError("Please complete all fields.")

                building = Building.objects.get(id=int(building_ids[i]))
                room = Room.objects.get(id=int(room_ids[i]), building=building)

                start_time = datetime.strptime(
                    start_times[i].strip(), '%H:%M'
                ).time()
                end_time = datetime.strptime(
                    end_times[i].strip(), '%H:%M'
                ).time()

                if end_time <= start_time:
                    raise ValueError(
                        f"Invalid time for {subject_names[i]}. "
                        "Start time must be earlier than end time."
                    )

                day_value = days[i].strip()

                # Check conflicts with existing schedules for this user
                conflict = Schedule.objects.filter(
                    user=request.user,
                    day_of_week=day_value,
                    start_time__lt=end_time,
                    end_time__gt=start_time,
                ).exists()

                if conflict:
                    raise ValueError(
                        f"{subject_names[i]} conflicts with an existing schedule."
                    )

                # Check conflicts with other schedules in the same submission
                for other in new_schedules:
                    if (
                        other['day_of_week'] == day_value
                        and other['start_time'] < end_time
                        and other['end_time'] > start_time
                    ):
                        raise ValueError(
                            f"{subject_names[i]} conflicts with another "
                            "submitted schedule."
                        )

                new_schedules.append({
                    'subject_name': subject_names[i].strip(),
                    'subject_code': subject_codes[i].strip(),
                    'room': room,
                    'day_of_week': day_value,
                    'start_time': start_time,
                    'end_time': end_time,
                })

            with transaction.atomic():
                for schedule in new_schedules:
                    Schedule.objects.create(
                        user=request.user,
                        entry_method=Schedule.EntryMethod.MANUAL,
                        **schedule,
                    )

            messages.success(request, 'Your schedules have been saved!')
            return redirect('create_schedule')

        except (
            ValueError,
            TypeError,
            IndexError,
            ValidationError,
            IntegrityError,
            Building.DoesNotExist,
            Room.DoesNotExist,
        ) as error:
            if isinstance(error, (Building.DoesNotExist, Room.DoesNotExist)):
                messages.error(request, "Invalid building or room selected.")
            elif isinstance(error, IntegrityError):
                messages.error(
                    request,
                    "Unable to save schedule due to a duplicate or conflicting record."
                )
            else:
                messages.error(request, str(error))

    schedules = Schedule.objects.filter(
        user=request.user
    ).order_by('day_of_week', 'start_time')

    buildings = Building.objects.all().order_by('building_name')

    rooms = Room.objects.select_related('building').all().order_by(
        'building__building_name',
        'room_number',
    )

    return render(
        request,
        'schedules/create_schedule.html',
        {
            'schedules': schedules,
            'buildings': buildings,
            'rooms': rooms,
        },
    )