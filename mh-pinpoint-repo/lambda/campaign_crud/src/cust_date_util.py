from datetime import datetime,timedelta
from dateutil import tz

def isGreaterThanToday(paramdate):
    dt1 = datetime.strptime(paramdate, "%Y%m%dT%H:%M%z")     
    tmpdt1 = datetime.strptime(paramdate, "%Y%m%dT%H:%M%z").replace(second=0, microsecond=0,tzinfo=None)
    curr = datetime.now(tz=dt1.timetz().tzinfo).replace(second=0, microsecond=0,tzinfo=None)
    if tmpdt1 > curr:
        return True     

 
def isEndGreatherThanStart(startdate,enddate):
    dt1 = datetime.strptime(startdate, "%Y%m%dT%H:%M%z")       
    dt2 = datetime.strptime(enddate, "%Y%m%dT%H:%M%z")    
    if dt2>dt1:
        return True

def getCurrentDateTime():
    return datetime.now(tz=tz.gettz('America/New_York')).strftime('%Y%m%dT%H%M%S%z')

def isStartDateBefore30Mts(paramdate):
    dt1 = datetime.strptime(paramdate, "%Y%m%dT%H:%M%z")     
    tmpdt1 = datetime.strptime(paramdate, "%Y%m%dT%H:%M%z").replace(second=0, microsecond=0,tzinfo=None)
    curr = datetime.now(tz=dt1.timetz().tzinfo).replace(second=0, microsecond=0,tzinfo=None) - timedelta(minutes=-30)
    print(tmpdt1)
    print(curr)
    if tmpdt1 >= curr:
        return True     
        