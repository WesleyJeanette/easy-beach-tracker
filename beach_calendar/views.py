from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import BeachCalendarEntry
import datetime
from calendar import monthcalendar, monthrange, month_name

# Create your views here.

def index(request):
    entries = BeachCalendarEntry.objects.all()
    entries = entries.order_by('-date')
    entries = entries[:10]  # Limit to the last 10 entries
    return render(request, 'index.html', {'entries': entries})

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
    
    my_calendar = []
    month_days = monthcalendar(start_date.year, start_date.month)
    for week in month_days:
        week_entries = []
        for day in week:
            if day == 0:
                week_entries.append(None)
            else:
                day_date = datetime.date(start_date.year, start_date.month, day)
                day_entries = BeachCalendarEntry.objects.filter(date=day_date)
                week_entries.append({'date': day, 'entries': day_entries})
        my_calendar.append(week_entries)
    return render(request, 'month_view.html', {
        'calendar': my_calendar,
        'month_name' : month_name[start_date.month],
        'year': start_date.year,
        })

def show_week(request):
    requested_week = request.GET.get('week')
    requested_year = request.GET.get('year')

    start_date = None
    end_date = None
    if requested_week and requested_year:
        # Calculate the start and end dates of the requested week
        week_number = int(requested_week)
        year = int(requested_year)
        start_date = datetime.date.fromisocalendar(year, week_number, 1)  # Monday of the week
        end_date = start_date + datetime.timedelta(days=6)  # Sunday of the week
    else:
        # If no week and year are provided, show the current week
        today = datetime.date.today()
        start_date = today - datetime.timedelta(days=today.weekday())  # Monday of the current week
        end_date = start_date + datetime.timedelta(days=6)  # Sunday of the current week
    
    entries = BeachCalendarEntry.objects.filter(date__gte=start_date, date__lte=end_date)
    entries = entries.order_by('-date')
    return render(request, 'week_view.html', {'entries': entries})

def entry_detail(request, entry_id):
    if request.method == 'POST':
        BeachCalendarEntry.objects.filter(id=entry_id).update(
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
        entry = BeachCalendarEntry.objects.get(id=entry_id)
        return render(request, 'entry_detail.html', {'entry': entry})
    if request.method == "DELETE":
        entry = get_object_or_404(BeachCalendarEntry, id=entry_id)
        entry.delete()
        return JsonResponse({'success': True})
    # else is a GET
    entry = BeachCalendarEntry.objects.get(id=entry_id)
    return render(request, 'entry_detail.html', {'entry': entry})

def add_entry(request):
    if request.method == 'POST':
        # Process the form data, in the future 
        # autofill some of the data, like tide, weather, etc.
        BeachCalendarEntry.objects.create(
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

        return render(request, 'index.html')

    # When the request method is GET, include any
    # recient beach names in the form
    recent_beach_names = BeachCalendarEntry.objects.values('beach').distinct().order_by('-date')[:5]
    return render(request, 'add_entry.html', {'recent_beach_names': recent_beach_names})

def edit_entry(request, entry_id):
    entry = BeachCalendarEntry.objects.get(id=entry_id)
    if request.method == 'PATCH':
        # Process the form data
        pass
    else:
        # Display the form
        pass
    return render(request, 'edit_entry.html', {'entry': entry})