from datetime import datetime


def attendance_entry(entry):
    # Extract information from the entry and return a tuple (name, date, time)
    name = entry.split('Name: ')[1].split('   ')[0].strip()
    date_str = entry.split('Date: ')[1].split('   ')[0].strip()
    time = entry.split('Time: ')[1].strip()
    date = datetime.strptime(date_str, '%A, %m/%d/%Y')
    return name, date, time
