import datetime as dt
from datetime import datetime as dt2

#面接を受けられる時間（10:00 ~ 18:00）
DAY_START_TIME = "T10:00:00+09:00"
DAY_END_TIME = "T18:00:00+09:00"

def calcEmptyDate(busy_times):
    busy_bit_data = changeScheduleToBit(busy_times)
    print(busy_bit_data)
    empty_times = getEmptyTimes(busy_bit_data)
    empty_times = getWholeEmptyTimes(empty_times)
    return empty_times

def changeScheduleToBit(busy_times):
    schedule_bit_data = {}
    for busy_time in busy_times:
        # list(date, bit_data)
        dateObj = changeEventToBit(busy_time)
        if dateObj['date'] not in schedule_bit_data.keys():
            schedule_bit_data[dateObj['date']] = dateObj['bit_data']
        else:
            schedule_bit_data[dateObj['date']] = makeLogicalSum(schedule_bit_data[dateObj['date']], dateObj['bit_data'])
    return schedule_bit_data


def changeEventToBit(busy_time):
    event_start_time = strToTime(busy_time['start'])
    event_end_time = strToTime(busy_time['end'])
    event_date = busy_time['start'][0:10]

    #1日の開始時刻・終了時刻
    day_start_time = strToTime(event_date + DAY_START_TIME)
    day_end_time = strToTime(event_date + DAY_END_TIME)
    day_time_diff = day_end_time - day_start_time

    # 30分ごとに分割する
    segment_count = int(day_time_diff.total_seconds() / 60 / 30)
    day_pointer = day_start_time

    print(segment_count)

    bit_data = ""
    for i in range(segment_count):
            if day_pointer > day_end_time:
                break
            if event_start_time  <= day_pointer and day_pointer < event_end_time:
                bit_data += "1"
            else:
                bit_data += "0"

            day_pointer += dt.timedelta(seconds=1800)
   
    return { "date": event_date, "bit_data": bit_data }




def strToTime(datetime):
    # datetime: 2020-03-02T15:00:00+09:00
    return dt2.strptime(datetime[:-6].replace('T', " "), '%Y-%m-%d %H:%M:%S')

def makeLogicalSum(bit_data1, bit_data2):
    logical_sum = ""
    for i in range(len(bit_data1)):
        bit1 = bit_data1[i]
        bit2 = bit_data2[i]
        if bit1 == "0" and bit2 == "0":
            logical_sum += "0"
        else:
            logical_sum += "1"
    return logical_sum

def getEmptyTimes(busy_times):
    empty_times = {}
    for key_date in busy_times:
        busy_time_bit_data = busy_times[key_date]
        day_start_time = strToTime(key_date + DAY_START_TIME)
        day_end_time = strToTime(key_date + DAY_END_TIME)
        day_pointer = day_start_time
        empty_start_time = None
        empty_end_time = None
        day_time_diff = day_end_time - day_start_time
        segment_count = int(day_time_diff.total_seconds() / 60 / 30)

        for i in range(segment_count):
            if busy_time_bit_data[i] == "0":
                if empty_start_time == None:
                    empty_start_time = day_pointer
                    day_pointer += dt.timedelta(seconds=1800)
                else:
                    if day_pointer < day_end_time - dt.timedelta(seconds=1800):
                        day_pointer += dt.timedelta(seconds=1800)
                    else:
                        empty_end_time = day_pointer
                        key = str(empty_start_time)[5:10]
                        if key not in empty_times:
                            empty_times[key] = []    
                        empty_times[key].append(str(empty_start_time)[11:-3] + " ~ " + str(empty_end_time + dt.timedelta(seconds=1800))[11:-3])
            elif busy_time_bit_data[i] == "1":
                if empty_start_time == None:
                    day_pointer += dt.timedelta(seconds=1800)
                else:
                    empty_end_time = day_pointer
                    key = str(empty_start_time)[5:10]
                    if key not in empty_times:
                        empty_times[key] = [] 
                    empty_times[key].append(str(empty_start_time)[11:-3] + " ~ " + str(empty_end_time)[11:-3])
                    empty_start_time = None
                    empty_end_time = None
                    day_pointer += dt.timedelta(seconds=1800)

    return empty_times

def getWholeEmptyTimes(empty_times):
    dt_now = dt2.now()
    for i in range(15):
        date = (dt_now + dt.timedelta(days=i))
        key = str(date)[5:10]
        if key not in empty_times:
            empty_times[key] = []
            empty_times[key].append("10:00 ~ 18:00")
    return empty_times







