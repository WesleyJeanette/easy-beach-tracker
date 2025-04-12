from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import BeachCalendarEntry
import datetime
from . import utils
import pandas as pd
from calendar import setfirstweekday, monthcalendar, monthrange, month_name

# Create your views here.

@login_required
def index(request):
    entries = BeachCalendarEntry.objects.filter(user=request.user).order_by('-date')[:10]
    return render(request, 'index.html', {'entries': entries})

@login_required
def show_month(request):
    requested_month = request.GET.get('month')
    requested_year = request.GET.get('year')

    start_date = None
    end_date = None
    if requested_month and requested_year:
        start_date = datetime.date(int(requested_year), int(requested_month), 1)
        end_date = datetime.date(int(requested_year), int(requested_month), monthrange(int(requested_year), int(requested_month))[1])
    else:
        # If no month and year are provided, show the current month
        today = datetime.date.today()
        current_month = today.month
        current_year = today.year
        start_date = datetime.date(current_year, current_month, 1)
        end_date = datetime.date(current_year, current_month, monthrange(current_year, current_month)[1])
    
    # Set the first day of the month
    setfirstweekday(6)  # Set Sunday as the first day of the week

    my_calendar = []
    month_days = monthcalendar(start_date.year, start_date.month)
    for week in month_days:
        week_entries = []
        for day in week:
            if day == 0:
                week_entries.append(None)
            else:
                day_date = datetime.date(start_date.year, start_date.month, day)
                day_entries = BeachCalendarEntry.objects.filter(user=request.user, date=day_date)
                week_entries.append({'date': day, 'entries': day_entries})
        my_calendar.append(week_entries)
    return render(request, 'month_view.html', {
        'calendar': my_calendar,
        'month_name' : month_name[start_date.month],
        'year': start_date.year,
        'today': datetime.date.today(),
        })

@login_required
def show_week(request):
    requested_week = request.GET.get('week')
    requested_year = request.GET.get('year')

    if requested_week and requested_year:
        # Calculate the start and end dates of the requested week
        week_number = int(requested_week)
        year = int(requested_year)
        start_date = datetime.date.fromisocalendar(year, week_number, 1)  # Monday of the week
    else:
        # If no week and year are provided, show the current week
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=today.weekday())  # Monday of the current week

    # Generate the week calendar
    week_entries = []
    for day_offset in range(7):  # Loop through the 7 days of the week
        day_date = start_date + datetime.timedelta(days=day_offset)
        day_entries = BeachCalendarEntry.objects.filter(user=request.user, date=day_date)
        week_entries.append({'date': day_date, 'entries': day_entries})

    return render(request, 'week_view.html', {
        'week_entries': week_entries,
        'start_date': start_date,
        'end_date': start_date + datetime.timedelta(days=6),  # Sunday of the week
        'today': datetime.date.today(),
    })

@login_required
def entry_detail(request, entry_id):
    if request.method == 'POST':
        visit_date = request.POST.get('date')
        visit_time = request.POST.get('time_of_visit')
        beach = request.POST.get('beach')

        # look up the beach location for the weather API
        # map of beachs to coordinates

        if request.POST.get('pull_conditions') == 'on':
            # In the future, we can pull weather conditions from an API
            visit_datetime = datetime.datetime.strptime(f"{visit_date} {visit_time}", "%Y-%m-%d %H:%M")

            marine = utils.collect_marine_weather_data(27.76, -80.401111)
            weather = utils.collect_weather_forcast_data(27.76, -80.401111)
            marine_match = marine.iloc[(marine['date'] - visit_datetime).abs().argsort()[:1]]
            weather_match = weather.iloc[(weather['date'] - visit_datetime).abs().argsort()[:1]]
            water_conditions = utils.describe_marine_weather_data(marine_match)
            weather_conditions = weather_match['temperature_2m'].values[0]
            air_temperature = weather_match['temperature_2m'].values[0]
            water_temperature = marine_match['sea_surface_temperature'].values[0]
            tide = marine_match['sea_level_height_msl'].values[0]
        else:
            water_conditions = request.POST.get('water_conditions')
            weather_conditions = request.POST.get('weather_conditions')
            air_temperature = request.POST.get('air_temperature')
            water_temperature = request.POST.get('water_temperature')
            tide = request.POST.get('tide')

        print(water_conditions, weather_conditions, air_temperature, water_temperature, tide)
        BeachCalendarEntry.objects.filter(id=entry_id, user=request.user).update(
            date=request.POST.get('date'),
            beach=request.POST.get('beach'),
            walked=request.POST.get('walked') == 'on',
            notes=request.POST.get('notes'),
            water_conditions=water_conditions,
            weather_conditions=request.POST.get('weather_conditions'),
            air_temperature=air_temperature,
            water_temperature=water_temperature,
            swam=request.POST.get('swam') == 'on',
            time_of_visit=request.POST.get('time_of_visit'),
            #duration=request.POST.get('duration'),
            tide=tide
        )
        entry = BeachCalendarEntry.objects.get(id=entry_id, user=request.user)
        return render(request, 'entry_detail.html', {'entry': entry})
    if request.method == "DELETE":
        entry = get_object_or_404(BeachCalendarEntry, id=entry_id, user=request.user)
        entry.delete()
        return JsonResponse({'success': True})
    # else is a GET
    entry = BeachCalendarEntry.objects.get(id=entry_id, user=request.user)
    return render(request, 'entry_detail.html', {'entry': entry})

@login_required
def add_entry(request):
    if request.method == 'POST':
        # Process the form data, in the future 
        # autofill some of the data, like tide, weather, etc.
        BeachCalendarEntry.objects.create(
            user=request.user,
            date=request.POST.get('date'),
            beach=request.POST.get('beach'),
            walked=request.POST.get('walked') == 'on',
            notes=request.POST.get('notes'),
            water_conditions=request.POST.get('water_conditions'),
            weather_conditions=request.POST.get('weather_conditions'),
            #air_temperature=request.POST.get('air_temperature'),
            #water_temperature=request.POST.get('water_temperature'),
            swam=request.POST.get('swam') == 'on',
            time_of_visit=request.POST.get('time_of_visit'),
            #duration=request.POST.get('duration'),
            #tide=request.POST.get('tide')
        )

        return redirect('home')

    # When the request method is GET, include any
    # recient beach names in the form
    recent_beach_names = BeachCalendarEntry.objects.filter(user=request.user).values('beach').distinct().order_by('-date')[:5]
    return render(request, 'add_entry.html', {'recent_beach_names': recent_beach_names})

@login_required
def edit_entry(request, entry_id):
    entry = BeachCalendarEntry.objects.get(id=entry_id)
    if request.method == 'PATCH':
        # Process the form data
        pass
    else:
        # Display the form
        pass
    return render(request, 'edit_entry.html', {'entry': entry})