import os
import re
import parse
import shutil
from datetime import datetime


def attendance_file(input_filename, output_folder):
    # Read the content of the input file
    with open(input_filename, 'r') as file:
        entries = file.readlines()

    # Parse entries and sort based on day of the week and date
    sorted_entries = sorted(entries, key=lambda x: parse.attendance_entry(x)[1:3])

    # Create new files and folders for each day of the week and date
    for entry in sorted_entries:
        name, date, time = parse.attendance_entry(entry)
        day_date = (date.strftime('%A'), date.strftime('%m-%d-%Y'))

        # Create a folder for the current day of the week and date only if it doesn't exist
        folder_name = os.path.join(output_folder, f'{day_date[0]}, {day_date[1]}')
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        # Create a new file in the folder with the same naming convention
        output_filename = os.path.join(folder_name, f'{day_date[0]}, {day_date[1]}.txt')
        with open(output_filename, 'a') as current_file:
            # Write the sorted entry to the current file
            current_file.write(f'Name: {name}   Date: {date.strftime("%A, %m/%d/%Y")}   Time: {time}\n')


def attendance_pictures(source_folder, destination_folder):
    # Create destination folder if not exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # List all files in the source folder
    files = os.listdir(source_folder)

    for file in files:
        file_path = os.path.join(source_folder, file)

        # Skip directories
        # if os.path.isdir(file_path):
            # continue

        # Check if the file is a JPG or PNG image
        if file.lower().endswith(('.jpg', '.png')):
            # Extract information from the filename using regular expression
            match = re.match(r'(.+?) {2}Date_(.+?) {2}Time_(.+?)\.(jpg|png)', file)

            # Check if the filename matches the expected pattern
            if match:
                name, date_str, time_str, extension = match.groups()

                # Convert date and time to datetime object
                datetime_obj = datetime.strptime(date_str + ' ' + time_str, '%A, %m-%d-%Y %I-%M-%S %p')

                # Create destination folder based on the day of the week and date
                date_folder = os.path.join(destination_folder, datetime_obj.strftime('%A, %m-%d-%Y'))

                # Create folder if not exists
                if not os.path.exists(date_folder):
                    os.makedirs(date_folder)

                # Copy the file to the destination folder
                destination_path = os.path.join(date_folder, file)
                shutil.copy(file_path, destination_path)
                # print(f'Copied {file} to {destination_path}')
