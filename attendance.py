from datetime import datetime


def write_name_date_time(file_name, name):
    current_date_time = datetime.now().strftime(f"Name: {name}   Date: %A, %m/%d/%Y   Time: %I:%M:%S %p")
    with open(file_name, 'a') as file:
        file.write(current_date_time + '\n')
