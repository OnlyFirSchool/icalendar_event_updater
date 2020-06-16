from icalendar import Calendar, Event, vDatetime
import datetime
import pytz
import sys

# Get earliest date from the calendar
def get_earliest_date_from_icalendar(gcal:Calendar) -> datetime.date:
    # Initialize unsorted list of dates
    list_of_dates = []
    for component in gcal.walk():
        if (component.name == 'VEVENT'):
            # get key value pairs of the component values
            for k,v in component.items():
                if k == 'DTSTART':
                    # If it is a datetime object, convert it to a date object
                    if isinstance(v.dt, datetime.datetime):
                        v_dt_dates = v.dt.date()
                        list_of_dates.append(v_dt_dates)
                    else:
                        list_of_dates.append(v.dt)
                if k == 'DTEND':
                    # If it is a datetime object, convert it to a date object
                    if isinstance(v.dt, datetime.datetime):
                        v_dt_dates = v.dt.date()
                        list_of_dates.append(v_dt_dates)
                    else:
                        list_of_dates.append(v.dt)

    # sort the list of dates by earliest date
    list_of_dates.sort(key = lambda d: datetime.datetime.strftime(d, "%y-%m-%d"))
    return list_of_dates[0]

# new_cal variable is the new Calendar object
def write_to_new_ics_file(new_cal) -> None:
    f = open('newCalendar.ics', 'wb')
    f.write(new_cal.to_ical())
    f.close()

def parse_and_convert_i_cal(file_name: str, start_date: datetime.date) -> None:
    try:
        events_of_calendar_l = []
        g = open(file_name, 'r', encoding='utf-8')

        # Make a new calendar
        new_cal = Calendar()

        # Initialize difference counter
        diff = 0;

        # Initialize time difference variable of new start date vs original starting date
        diff_btwn_dates = start_date

        gcal = Calendar.from_ical(g.read())

        # Get earliest calendar date from file
        earliest_date = get_earliest_date_from_icalendar(gcal)

        # Get date delta and implement the difference to other dates
        diff_btwn_dates = abs(start_date - earliest_date)

        # Get each event name and add it to a list
        for component in gcal.walk():
            if(component.name == 'VCALENDAR'):
                # get key value pairs of the component values
                for k,v in component.items():
                    new_cal.add(k, v)

            if(component.name == 'VEVENT'):
                # Increment diff counter after every VEVENT is found
                diff += 1
                # Initialize new event
                event = Event()

                # get key value pairs of the component values
                for k,v in component.items():
                    if k == 'DTSTART':
                        new_date = v.dt + datetime.timedelta(days=diff_btwn_dates.days)
                        event.add(k, new_date)
                    elif k == 'DTEND':
                        new_date = v.dt + datetime.timedelta(days=diff_btwn_dates.days)
                        event.add(k, new_date)

                    elif k =='RRULE':
                        # Loop through RRULE object
                        for key, value in v.items():
                            # Add the frequencies to the RRULE values depending on its occurrence (minutely, hourly, daily, weekly, monthly, or yearly)
                            if key == 'FREQ':
                                if v['FREQ'] == ['MINUTELY']:
                                    event.add(k, {'FREQ': ['MINUTELY']})
                                if v['FREQ'] == ['HOURLY']:
                                    event.add(k, {'FREQ': ['HOURLY']})
                                if v['FREQ'] == ['DAILY']:
                                    event.add(k, {'FREQ': ['DAILY']})
                                if v['FREQ'] == ['WEEKLY']:
                                    event.add(k, {'FREQ': ['WEEKLY']})
                                if v['FREQ'] == ['MONTHLY']:
                                    event.add(k, {'FREQ': ['MONTHLY']})
                                if v['FREQ'] == ['YEARLY']:
                                    event.add(k, {'FREQ': ['YEARLY']})
                    else:
                        event.add(k, v)

                # add sub component to new calendar
                new_cal.add_component(event)

        # write all the data to a new ics file
        write_to_new_ics_file(new_cal)
        print("Calendar updated successfully!")
        g.close()

    except FileNotFoundError:
        print("File Not Found!")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        year, month, day = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        d = datetime.date(year, month, day)
        parse_and_convert_i_cal(file_name, d)


