import cv2
import glob
import os
from threading import Thread
from emailing import send_email

video = cv2.VideoCapture(0)
first_frame = None
status_list = list()
count = 1

def clean_folder():
    print("clean_folder started")
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)
    print("clean_folder ended")

while True:
    status = 0
    # time.sleep(1)
    check, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame,(21,21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    thresh_frame = cv2.threshold(delta_frame, 55, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My Video", dil_frame)
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 4000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"Images/{count}.png", frame)
            count += 1
            all_images = glob.glob("Images/*.png")
            index = int(len(all_images)/2)
            image_with_object = all_images[index]


    status_list.append(status)
    status_list = status_list[-2:]
    print(status_list)

    if status_list == [1, 0]:
        email_thread = Thread(target=send_email, args=(image_with_object,))
        email_thread.daemon = True
        # send_email(image_with_object)
        clean_thread = Thread(target=clean_folder, )
        clean_thread.daemon = True
        # clean_folder()

        email_thread.start()


    cv2.imshow("Video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break

clean_thread.start()
video.release()
