
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from datetime import datetime

from .models import Schedule, Building, Room


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
            end_times
        ]

        try:

            # Check if all fields have matching entries
            if not subject_names or any(
                len(field) != len(subject_names)
                for field in field_lists
            ):
                raise ValueError(
                    "Please complete all schedule fields."
                )

            new_schedules = []

            # Validate each submitted schedule
            for i in range(len(subject_names)):

                if not all([
                    subject_names[i].strip(),
                    subject_codes[i].strip(),
                    room_ids[i],
                    building_ids[i],
                    days[i],
                    start_times[i],
                    end_times[i]
                ]):
                    raise ValueError(
                        "Please complete all fields."
                    )

                # Get selected building and room
                building = Building.objects.get(
                    id=building_ids[i]
                )

                room = Room.objects.get(
                    id=room_ids[i],
                    building=building
                )

                # Convert time strings into time objects
                start_time = datetime.strptime(
                    start_times[i], '%H:%M'
                ).time()

                end_time = datetime.strptime(
                    end_times[i], '%H:%M'
                ).time()

                # Check start and end time
                if end_time <= start_time:
                    raise ValueError(
                        f"Invalid time for {subject_names[i]}. "
                        "Start time must be earlier than end time."
                    )

                # Check conflicts with existing schedules
                conflict = Schedule.objects.filter(
                    user=request.user,
                    day_of_week=days[i],
                    start_time__lt=end_time,
                    end_time__gt=start_time
                ).exists()

                if conflict:
                    raise ValueError(
                        f"{subject_names[i]} conflicts with an existing schedule."
                    )

                # Check conflicts with other submitted schedules
                for other in new_schedules:

                    if (
                        other['day_of_week'] == days[i]
                        and other['start_time'] < end_time
                        and other['end_time'] > start_time
                    ):
                        raise ValueError(
                            f"{subject_names[i]} conflicts with another "
                            "submitted schedule."
                        )

                # Store validated schedule temporarily
                new_schedules.append({
                    'subject_name': subject_names[i],
                    'subject_code': subject_codes[i],
                    'room': room,
                    'day_of_week': days[i],
                    'start_time': start_time,
                    'end_time': end_time
                })

            # Save schedules only after all pass validation
            with transaction.atomic():

                for schedule in new_schedules:
                    Schedule.objects.create(
                        user=request.user,
                        entry_method=Schedule.EntryMethod.MANUAL,
                        **schedule
                    )

            messages.success(
                request,
                'Your schedules have been saved!'
            )

            return redirect('create_schedule')

        except (
            ValueError,
            IndexError,
            Building.DoesNotExist,
            Room.DoesNotExist
        ) as error:

            if isinstance(
                error,
                (Building.DoesNotExist, Room.DoesNotExist)
            ):
                messages.error(
                    request,
                    "Invalid building or room selected."
                )
            else:
                messages.error(
                    request,
                    str(error)
                )

    # Retrieve existing schedules
    schedules = Schedule.objects.filter(
        user=request.user
    ).order_by('day_of_week', 'start_time')

    # Retrieve buildings and rooms for dropdowns
    buildings = Building.objects.all().order_by(
        'building_name'
    )

    rooms = Room.objects.select_related(
        'building'
    ).all().order_by(
        'building__building_name',
        'room_number'
    )

    return render(
        request,
        'schedules/create_schedule.html',
        {
            'schedules': schedules,
            'buildings': buildings,
            'rooms': rooms
        }
    )
