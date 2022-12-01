from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.card import MDCard


import AppAPIRequest as function
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import  Layout
#import uix components
from kivy.uix.image import Image, AsyncImage
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
import cv2
from kivy.properties import StringProperty
import threading
from functools import partial
import sys
import mediapipe as mp

'''Importando el modulo para que ejercicio se esta llamando'''
import CaseExercise as caseExercise

#import other kivy stuff
from kivy.clock import Clock


usernameglobal = ''
#Guardando el token en una variable para luego realizar las peticiones
token = ''
#El ejercicio a realizar
ejercicio = 'Flexion codo'
tipo = 'fortalecimiento'
parte = 'superior'
amount = 2
serie = 1
class MenuScreen(Screen):

    '''def update_info(self, username, password):
            self.token = '''

    def login(self, username, password):
        print('el print')
        #print(MDApp.get_running_app().root.manager.MY_GLOBAL)
        global usernameglobal
        global token

        if(username != '' and password != ''):
            #guardando el token
            token = function.AppAPIRequest.calllogin(self, username, password)
            if token != 500 and token != 0 and token != '':
                MDApp.get_running_app().root.current = 'listExercise'
            else:
                print('Hubo problemas en la autenticacion')

            if(token!=''):
                usernameglobal = username
            print(username + '----' + password)
        else:
            print('Por favor llenar las casillas')



class VideoScreen(Screen):
    def on_enter(self):
        #en este treading hacer lo del switch tambie, osea que al escoger tren inferior o algo active el threading de
        # self.parte inferior fortalecimiento o algo asi
        if parte == 'superior' and tipo == 'elongacion':
            threading.Thread(target=self.doSuperiorElong, daemon=True).start()

        elif parte == 'superior' and tipo == 'fortalecimiento':
            threading.Thread(target=self.doSuperiorFort, daemon=True).start()

        elif parte == 'inferior' and tipo == 'elongacion':
            threading.Thread(target=self.doInferiorLong, daemon=True).start()

        elif parte == 'inferior' and tipo == 'fortalecimiento':
            threading.Thread(target=self.doInferiorFort, daemon=True).start()

    def doSuperiorFort(self, *args):
        # this code is run in a separate thread
        self.do_vid = True  # flag to stop loop
        self.cam = cv2.VideoCapture(1)

        while (self.do_vid):
            global ejercicio, serie, amount
            ret, frame = self.cam.read()

            frame = caseExercise.switch_superior_fortalecimiento(frame, ejercicio, amount, serie)
            # the partial function just says to call the specified method with the provided argument (Clock adds a time argument)
            Clock.schedule_once(partial(self.display_frame, frame))

            #cv2.imshow('Hidden', frame)
            #cv2.waitKey(1)
        self.cam.release()
        cv2.destroyAllWindows()

    def doSuperiorElong(self, *args):
        # this code is run in a separate thread
        self.do_vid = True  # flag to stop loop
        self.cam = cv2.VideoCapture(1)

        while (self.do_vid):
            global ejercicio, serie, amount
            ret, frame = self.cam.read()

            frame = caseExercise.switch_superior_elongacion(frame, ejercicio, amount, serie)
            # the partial function just says to call the specified method with the provided argument (Clock adds a time argument)
            Clock.schedule_once(partial(self.display_frame, frame))

            #cv2.imshow('Hidden', frame)
            #cv2.waitKey(1)
        self.cam.release()
        cv2.destroyAllWindows()

    def doInferiorFort(self, *args):
        # this code is run in a separate thread
        self.do_vid = True  # flag to stop loop
        self.cam = cv2.VideoCapture(1)

        while (self.do_vid):
            global ejercicio, serie, amount
            ret, frame = self.cam.read()

            frame = caseExercise.switch_inferior_fortalecimiento(frame, ejercicio, amount, serie)
            # the partial function just says to call the specified method with the provided argument (Clock adds a time argument)
            Clock.schedule_once(partial(self.display_frame, frame))

            #cv2.imshow('Hidden', frame)
            #cv2.waitKey(1)
        self.cam.release()
        cv2.destroyAllWindows()

    def doInferiorLong(self, *args):
        # this code is run in a separate thread
        self.do_vid = True  # flag to stop loop
        self.cam = cv2.VideoCapture(1)
        while (self.do_vid):
            global ejercicio, serie, amount
            ret, frame = self.cam.read()

            frame = caseExercise.switch_inferior_elongacion(frame, ejercicio, amount, serie)
            # the partial function just says to call the specified method with the provided argument (Clock adds a time argument)
            Clock.schedule_once(partial(self.display_frame, frame))

            #cv2.imshow('Hidden', frame)
            #cv2.waitKey(1)
        self.cam.release()
        cv2.destroyAllWindows()

    def stop_vid(self):
        # stop the video capture loop
        self.do_vid = False
        self.cam.release()

    def display_frame(self, frame, dt):
        # display the current video frame in the kivy Image widget

        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')

        # copy the frame data into the texture
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')

        # flip the texture (otherwise the video is upside down
        texture.flip_vertical()

        # actually put the texture in the kivy Image widget
        self.ids.vid.texture = texture






class ListExerciseScreen(Screen):
    def on_enter(self):
        global usernameglobal, token
        listaEjercicios = function.AppAPIRequest.calllist(self, token, usernameglobal)
        # verificando que la lista este llena
        if listaEjercicios != 500 and listaEjercicios != 0 and listaEjercicios != '':
            for element in listaEjercicios:  # iteramos sobre data
                #icon = AsyncImage(source=str(element['ejercicioId']['linkImagenFinal']))
                self.button = Button(
                    background_color= (255, 255, 255, 0),
                    #on_press = lambda x, item=element: print("\nitem number\n", item),
                    on_press = lambda x, item = element: self.click(item),
                    pos=self.parent.pos,
                    size=self.parent.size
                )
                self.asyncImage = AsyncImage(
                    source=str(element['ejercicioId']['linkImagenFinal']),
                    pos = self.parent.pos,
                    size = self.parent.size
                )

                self.mdcard = MDCard(
                    size_hint= (.6, .6),
                    pos_hint= {'center_x': .5, 'center_y': .40}
                )
                #Ingresando la el boton dentro de la imagen y la imagen dentro del card
                #luego agregando el card al carousel
                self.asyncImage.add_widget(self.button)
                self.mdcard.add_widget(self.asyncImage)
                carousel = self.ids.carousel
                carousel.add_widget(self.mdcard)


        else:
            print('Hubo problemas en la autenticacion')

    def click(self, item):
        global parte, tipo, ejercicio
        parte = item['ejercicioId']['parteCuerpo']
        tipo = item['ejercicioId']['tipo']
        ejercicio = item['ejercicioId']['nombre']

        MDApp.get_running_app().root.current = 'video'

        print(item['ejercicioId']['nombre'])





# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(VideoScreen(name='video'))
sm.add_widget(ListExerciseScreen(name='listExercise'))


class DemoApp(MDApp):

    def build(self):
        screen = Builder.load_file('ScreensApp.kv')
        return screen




DemoApp().run()