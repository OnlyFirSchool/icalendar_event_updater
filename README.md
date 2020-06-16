# iCalendar Date Conversion

## Setting Up
* Make sure to have **python3.7** installed and placed in the environmental variables for **Windows/Mac/Linux**

## Running date_conversion.py On The Command Line/Shell
1. Run "**python date_conversion.py [ARGUMENT 1] [ARGV...]**" on a shell or Windows terminal
    **In case the command **python** isn't recognized, try **python3.7** instead*
2. **ARGUMENT 1**: ICS file (must be within the same directory as date_conversion.py)
3. **ARGV...:** Start Date using the format: **year, month, day** (e.g. 2020 06 15)

## New Calendar File
* If the program successfully runs, **newCalendar.ics** will be created in the same directory with the updated events


## Issues
* VTimezone events can be parsed, but I could not figure out a way to rewrite the data to a new file. The documentation from iCalendar states that it is possible to add new VCALENDAR components with VEVENT subcomponents.  However, it does not provide any documentation or use cases for the Timezone component.
