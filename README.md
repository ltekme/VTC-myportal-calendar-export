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

### create .config (optional)

This script is used for automation. Note, a working screen is needed for chrome to do it's thing.

Wihen the 2 values are persent, the script will automatically fill in the 2 input boxes otherwise manule login from the broswer is needed.

1. rename `.config.template` to `.config`
2. replace `<-replace with cna->` with your CNA
3. replace `<-replace with password->` with your CNA password

or

you can set the following varable in your terminal with theire value

- `CALENDER_CNA`: CNA
- `CALENDER_PASSWORD`: Password

### Replacing Calender start and end date

in `extract.py` there is 2 varable

1. `CALENDER_START_DATE`
2. `CALENDER_END_DATE`

All events will be extracted between `CALENDER_START_DATE` and `CALENDER_END_DATE`. Note:

- The format is `YYYYMMDD` e.g. `20240601`. 
- `CALENDER_START_DATE` is earler then `CALENDER_END_DATE`
- The delta between `CALENDER_START_DATE` and `CALENDER_END_DATE` must be grater then 1 day.

If these condition arn't met, API error will respond with an error. API calls are made directly from the 2 values.

DO NOT MESS IT UP

DO NOT MESS IT UP

DO NOT MESS IT UP

### Adjusting Filter

between line `120` and `124`

``` python
# filter holiday
calender_events = [x for x in calender_events if x['eventType'] != 'Holiday']
calender_events = [x for x in calender_events if x['eventType'] != 'InstitutionHoliday']
```

This block of code exist. line `122` filter the event type of Holiday and line `123` filter Campus holiday. Comment out each one to select what not to filter.

### Adjust Exported file names as needed

By running the script 2 files will be generated. 

- `calender_events.json`
- `myportal_bot-{time created}-{CALENDER_START_DATE}_{CALENDER_END_DATE}`

these 2 can be changed to whatever.

## Executing the script

After everything is adjusted as needed. Execute

``` cmd
python extract.py
```

If you have done the `create .config (optional)` step. A chrome window will open up. If the cna or password is incorrect, manule login is needde.

Else if you did not. A chrome winodw will pop up and you need to login manualy.

After loggin in a serious of clicks will be executed to obtain the api url for event informaton.

If `calender_events.json` is present in the directory of the script. No broswer will be opened. This file holds all events extracted from myportal, so when the script is excuted again it will not go to myportal again to fetch the data.

To get new data delete the existing `calender_events.json` and execute the scrip.

Once Event data is fetched. The scrip will generate an iCal file which can be imported to calender apps such as google calendar.

## importing to google calendar

I am still working on createing a cloud function to synce the data between the 2 calendar. So far the most relicble solution is to create a new calender and import the ics to the new calender to prevent messing up your existing one.

## Disclaimer

I am not responsable for anything done to your account. Please exercise accordding to your own knoledge. It is not recommented to sotre credentials as plain text. Please read through the scrip before executing to make sure it has not been modified to send any data to anyware other then myportal.

Happy tooling.
