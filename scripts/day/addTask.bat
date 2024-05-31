@echo off
set scriptPath=D:\mxz\mxz_back\scripts\day\day_photo2.py
set taskName=MyTask

schtasks /create /tn %taskName% /tr %scriptPath% /sc daily /st 19:00 /du 23:59 /ri 30 /f
