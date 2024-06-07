# VTC-myportal-calendar-export

An small script to extract the calendar in myportal into an ical file to be imported into other calendar apps.

## init

Download this repo and extract it to an empty folder.

Make sure you have a working version of chrome. Last tested version: 123.0.6312.60

Make sure you have python installed.

If so. execure the following command to install python dependences

```
pip install -r requirements.txt
```

## Extracting ical file

### .config.template

This a template file for `.config`. Not every define is used, only copy what you need. See below for more details.

### auto login setup (optional)

This script is used for automation. Note, a working screen is needed for chrome to do it's thing.

When the 2 values are persent, the script will automatically fill in the 2 input boxes otherwise manule login from the broswer is needed.

`-` `CALENDER_CNA`: `CNA`
- - `CALENDER_PASSWORD`: `Passwor`- - `d`

The 2 varable will also follow enviroment varable.

### Replacing Calender start and end date

In the .config for additional varable can be defined

- `CALENDER_END_DATE` default: `20240516`
- `CALENDER_START_DATE` default: `20240730`

The 2 varable will follow enviroment varable when not set will follow values in extract.py

All events will be extracted between `CALENDER_START_DATE` and `CALENDER_END_DATE`. Note:

- The format is `YYYYMMDD` e.g. `20240601`. 
- `CALENDER_START_DATE` is earler then `CALENDER_END_DATE`
- The delta between `CALENDER_START_DATE` and `CALENDER_END_DATE` must be grater then 1 day.

If these condition arn't met, API error will respond with an error. API calls are made directly from the 2 values.

DO NOT MESS IT UP

DO NOT MESS IT UP

DO NOT MESS IT UP

### Adjusting Filter

between line `117` and `118`

``` python
# filter holiday
    calender_events = list(filter(lambda e: e['eventType'] != 'Holiday', calender_events))
    calender_events = list(filter(lambda e: e['eventType'] != 'InstitutionHoliday', calender_events))
```

This block of code exist. line `117` filter the event type of Holiday and line `118` filter Campus holiday. Comment out each one to select what not to filter.

### Adjust Exported file names as needed

In .config these 2 varable can be used to defined exported file names

- `CALENDER_EVENTS_FILE` default: `calender_events.json`
- `CALENDER_EXPORT_FILE` default: `calender_export.ics`

The 2 varable will follow enviroment varable when not set will follow values in extract.py

## Executing the script

After everything is adjusted as needed. Execute

``` cmd
python extract.py
```

If you have done the `auto login setup (optional)` step. A chrome window will open up. If the cna or password is incorrect, manule login is needde.

Else if you did not. A chrome winodw will pop up and you need to login manualy.

After loggin in a serious of clicks will be executed to obtain the api url for event informaton.

If `CALENDER_EVENTS_FILE` is present in the directory of the script. No broswer will be opened. This file holds all events extracted from myportal, so when the script is excuted again it will not go to myportal again to fetch the data.

To get new data delete the existing `CALENDER_EVENTS_FILE` and execute the scrip.

Once Event data is fetched. The scrip will generate an iCal file which can be imported to calender apps such as google calendar.

## importing to google calendar

I am still working on createing a cloud function to synce the data between the 2 calendar. So far the most relicble solution is to create a new calender and import the ics to the new calender to prevent messing up your existing one.

## filtering by modules

You can define the following vars in .config

- `CALENDER_FILTER_MODULE` default: 'ITP4927'
- `CALENDER_EVENTS_FILE` default: 'calender_events.json'
- `CALENDER_FILTERED_EVENTS_FILE` default: f'{CALENDER_FILTER_MODULE}_events.json'
- `CALENDER_FILTERED_EXPORT_FILE` default: f'{CALENDER_FILTER_MODULE}_events.ics'

These varable will follow evnv when not set, the default in `filter_module.py`

once selected execute

``` bash
python filter_module.py
```

This will create 2 files

- f'{CALENDER_FILTER_MODULE}_events.json'
   contains filtered events in the calendar

- f'{CALENDER_FILTER_MODULE}_events.ics'
   an ics of filtered modules that can be imported to calendar apps

## Disclaimer

I am not responsable for anything done to your account. Please exercise accordding to your own knoledge. It is not recommented to sotre credentials as plain text. Please read through the scrip before executing to make sure it has not been modified to send any data to anyware other then myportal.

Happy tooling.
