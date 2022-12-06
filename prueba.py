'''from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

import numpy as np
import matplotlib.pyplot as plt
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas


def enter_axes(event):
    print('enter_axes', event.inaxes)
    event.inaxes.patch.set_facecolor('yellow')
    event.canvas.draw()


def leave_axes(event):
    print('leave_axes', event.inaxes)
    event.inaxes.patch.set_facecolor('white')
    event.canvas.draw()


def enter_figure(event):
    print('enter_figure', event.canvas.figure)
    event.canvas.figure.patch.set_facecolor('red')
    event.canvas.draw()


def leave_figure(event):
    print('leave_figure', event.canvas.figure)
    event.canvas.figure.patch.set_facecolor('grey')
    event.canvas.draw()


kv = """
<Test>:
    orientation: 'vertical'
    Button:
        size_hint_y: None
        height: 40
"""

Builder.load_string(kv)


class Test(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        self.add_plot()

    def get_fc(self, i):
        fig1 = plt.figure()
        fig1.suptitle('mouse hover over figure or axes to trigger events' +
                      str(i))
        ax1 = fig1.add_subplot(211)
        ax2 = fig1.add_subplot(212)
        wid = FigureCanvas(fig1)
        fig1.canvas.mpl_connect('figure_enter_event', enter_figure)
        fig1.canvas.mpl_connect('figure_leave_event', leave_figure)
        fig1.canvas.mpl_connect('axes_enter_event', enter_axes)
        fig1.canvas.mpl_connect('axes_leave_event', leave_axes)
        return wid

    def add_plot(self):
        self.add_widget(self.get_fc(1))
        self.add_widget(self.get_fc(2))


class TestApp(App):
    def build(self):
        return Test()

if __name__ == '__main__':
    TestApp().run()'''

'''import cv2
from datetime import datetime

# the duration (in seconds)
duration = 5
cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
print(cv2.CAP_DSHOW)
print(cap)
qu = 0
while True:

    ret, frame = cap.read()
    start_time = datetime.now()
    diff = (datetime.now() - start_time).seconds  # converting into seconds
    while (diff <= duration):
        ret, frame = cap.read()
        cv2.putText(frame, str(diff), (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                    cv2.LINE_AA)  # adding timer text
        cv2.imshow('frame', frame)
        diff = (datetime.now() - start_time).seconds




        k = cv2.waitKey(10)
        if k & 0xFF == ord("r"):  # reset the timer
            break
        if k & 0xFF == ord("q"):  # quit all
            qu = 1
            break

    if qu == 1:
        break

cap.release()
cv2.destroyAllWindows()
'''


import cv2
import sys
from datetime import datetime

# Initialize variables
camSource = 1
running = True
saveCount = 0
nSecond = 0
totalSec = 3
strSec = '321'
keyPressTime = 0.0
startTime = 0.0
timeElapsed = 0.0
startCounter = False
endCounter = False

# Start the camera
camObj = cv2.VideoCapture(camSource)
if not camObj.isOpened():
    sys.exit('Camera did not provide frame.')

frameWidth = 800
frameHeight = 800

# Start video stream
while running:
    readOK, frame = camObj.read()

    # Display counter on screen before saving a frame
    if startCounter:
        if nSecond < totalSec:
            # draw the Nth second on each frame
            cv2.putText(img = frame,
                        text = strSec[nSecond],
                        org = (int(frameWidth/2 - 20),int(frameHeight/2)),
                        fontFace = cv2.FONT_HERSHEY_DUPLEX,
                        fontScale = 6,
                        color = (255,255,255),
                        thickness = 5)

            timeElapsed = (datetime.now() - startTime).total_seconds()
#            print 'timeElapsed: {}'.format(timeElapsed)

            if timeElapsed >= 1:
                nSecond += 1
#                print 'nthSec:{}'.format(nSecond)
                timeElapsed = 0
                startTime = datetime.now()
            print("TIME ELAPSED "+str(nSecond))

        else:
            cv2.imwrite('img' + str(saveCount) + '.jpg', frame)
#            print 'saveTime: {}'.format(datetime.now() - keyPressTime)
            saveCount += 1
            startCounter = False
            nSecond = 1

    # Get user input
    keyPressed = cv2.waitKey(3)
    if keyPressed == ord('s'):
        startCounter = True
        startTime = datetime.now()
        keyPressTime = datetime.now()
#        print 'startTime: {}'.format(startTime)
#        print 'keyPressTime: {}'.format(keyPressTime)

    elif keyPressed == ord('q'):
        # Quit the while loop
        running = False
        cv2.destroyAllWindows()

    # Show video stream in a window
    cv2.imshow('video', frame)

camObj.release()




