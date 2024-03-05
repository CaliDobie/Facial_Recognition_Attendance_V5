import os
import cv2
import load
import read
import sort
import write
import folder
import keyboard
import recognize
import attendance as at
from datetime import datetime


main = r"\your\folder\path\here"
temp_folder = fr"{main}\Temp"
known_faces_folder = fr"{main}\Known_Faces"
temp_picture = fr"{main}\Temp\picture.jpg"
attendance_pictures = fr"{main}\Attendance\Attendance_Pictures"
attendance = fr"{main}\Attendance\Attendance.txt"
attendance_backup = fr"{main}\Attendance\Attendance_Backup\Attendance.txt"
sorted_attendance = fr"{main}\Sorted_Attendance"

width = 640  # Width value
height = 480  # Height value
frames = 60  # Frame rate value(fps)

# Open a connection to the camera (0 is the default camera)
camera_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # cv2.CAP_DSHOW opens camera faster
camera_capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)  # Sets the width
camera_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)  # Sets the height
camera_capture.set(cv2.CAP_PROP_FPS, frames)  # Sets the frame rate

while True:
    # Capture each frame from the camera
    _, frame = camera_capture.read()

    # Display the frame in a preview window
    cv2.imshow("A = Attendance, F = New Folder, P = New Picture, D = Delete Picture, Esc = Sort & Close", frame)

    # Check for a key press
    if keyboard.is_pressed("a"):  # Attendance capture
        # Temp image name
        image_name = "picture.jpg"

        # Specify the path where the image will be saved
        image_path = os.path.join(temp_folder, image_name)

        # Save the captured frame as an image
        cv2.imwrite(image_path, frame)

        print("loading...")

        known_faces, known_names = load.saved_known_faces(known_faces_folder)
        name = recognize.face(temp_picture, known_faces, known_names)

        # Takes attendance in txt file
        at.write_name_date_time(attendance, name)
        at.write_name_date_time(attendance_backup, name)

        # Date and time as a string
        name_date_time = datetime.now().strftime(f"Name_{name}  Date_%A, %m-%d-%Y  Time_%I-%M-%S %p.jpg")

        # Attendance image name
        image_name = name_date_time

        # Specify the path where the image will be saved
        image_path = os.path.join(attendance_pictures, image_name)

        # Save the captured frame as an image
        cv2.imwrite(image_path, frame)

    # Check for f key press
    if keyboard.is_pressed("f"):  # new personal folder in known faces folder
        # Allow the user to input a name for the folder
        folder_name = input("Enter the name for the folder: ")

        # Create the folder
        folder.create(known_faces_folder, folder_name)

    # Check for p key press
    if keyboard.is_pressed("p"):  # New picture in personal folder
        folder_name = input("Enter the person's name: ")

        # Loads personal folder path
        personal_folder_path = known_faces_folder + "\\" + folder_name
        # Loads count.txt path
        count_file_path = known_faces_folder + "\\" + folder_name + r"\count.txt"

        # Check if the path exists
        if os.path.exists(personal_folder_path and count_file_path):
            # Reads count from count.txt
            count = read.count_from_file(count_file_path)

            # Increment count
            count += 1

            # Specify the path where the image will be saved
            image_path = os.path.join(personal_folder_path, f"{count}.jpg")

            # Save the captured frame as an image
            cv2.imwrite(image_path, frame)

            print("Picture saved.")
            print("\n")

            # Updates count in count.txt
            write.count_to_file(count_file_path, count)

        else:
            print(f"The folder for '{folder_name}' does not exist.")
            print("\n")

    # Check for d key press
    if keyboard.is_pressed("d"):  # Delete last picture in personal folder
        folder_name = input("Enter the person's name: ")

        # Loads personal folder path
        personal_folder_path = known_faces_folder + "\\" + folder_name
        # Loads count.txt path
        count_file_path = known_faces_folder + "\\" + folder_name + r"\count.txt"

        # Check if the path exists
        if os.path.exists(personal_folder_path and count_file_path):
            # Reads count from count.txt
            count = read.count_from_file(count_file_path)

            # Checks to make sure count isn't 0
            if count > 0:
                # Specify the path where the image will be deleted from
                image_path = os.path.join(personal_folder_path, f"{count}.jpg")

                # Delete the image at the path
                os.remove(image_path)

                # Decrement count
                count -= 1

                print("Picture deleted.")
                print("\n")

                # Updates count in count.txt
                write.count_to_file(count_file_path, count)

            # if count is 0
            else:
                print("There are no pictures in the folder.")
                print("\n")

        else:
            print(f"The folder for '{folder_name}' does not exist.")
            print("\n")

    # Check for Esc key press
    if cv2.waitKey(1) & 0xFF == 27:
        sort.attendance_file(attendance, sorted_attendance)  # Sorts attendance txt file
        sort.attendance_pictures(attendance_pictures, sorted_attendance)  # Sorts attendance pictures
        break  # Exits

# Release the camera and close OpenCV windows
camera_capture.release()
cv2.destroyAllWindows()
