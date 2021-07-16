import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog
#import mail
import time
import datetime
import smtplib


def send_email(subject, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("sravyasuren@gmail.com", "theboldtype")
        message = 'Subject: {}\n\n{}'.format(subject, msg)
        server.sendmail("sravyasuren@gmail.com", "srisravya484@gmail.com", message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")


root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
cap = cv.VideoCapture(file_path)
frame_width = int( cap.get(cv.CAP_PROP_FRAME_WIDTH))

frame_height =int( cap.get( cv.CAP_PROP_FRAME_HEIGHT))

#fourcc = cv.VideoWriter_fourcc('X','V','I','D')
fourcc = cv.VideoWriter_fourcc(*'XVID')

out = cv.VideoWriter("output.avi", fourcc, 5.0, (1280,720))


ret, frame1 = cap.read()
ret, frame2 = cap.read()
print(frame1.shape)
print(frame2.shape)
while cap.isOpened():
    diff = cv.absdiff(frame1, frame2)
    gray = cv.cvtColor(diff, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dilated = cv.dilate(thresh, None, iterations=3)
    contours, _ = cv.findContours(dilated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        (x, y, w, h) = cv.boundingRect(contour)

        if cv.contourArea(contour) < 900:
            continue
        cv.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv.putText(frame1, "Status: {}".format('Intruder Detected'), (10, 20), cv.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 3)

    image = cv.resize(frame1, (1280,720))
    out.write(image)
    cv.imshow("Detecting....", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv.waitKey(25) & 0xFF == ord('q'):
        break

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d, %H:%M:%S')
send_email("⚠⚠INTRUDER DETECTED⚠⚠", "Hello!\n intruder has been detected from source at " + st + ". ""\nStay safe,\nTresspassing Detection Team")

cv.destroyAllWindows()
cap.release()
out.release()
