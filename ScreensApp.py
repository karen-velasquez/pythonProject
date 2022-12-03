from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
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
from kivy.uix.dropdown import DropDown
import cv2
from kivy.properties import StringProperty
import threading
from functools import partial
'''Importando el modulo para que ejercicio se esta llamando'''
import CaseExercise as caseExercise
import CameraChoose as cameraChoose
#import other kivy stuff
from kivy.clock import Clock
from kivy.uix.popup import Popup

import tkinter
window = tkinter.Tk()
window.title("GUI")





usernameglobal = ''
#Guardando el token en una variable para luego realizar las peticiones
token = ''
#El ejercicio a realizar
ejercicio = 'Sentadilla'
tipo = 'fortalecimiento'
parte = 'inferior'
amount = 2
serie = 1

'''------ Creando el Pop-Up -------'''
class PopUpCamera(FloatLayout):
    def on_enter(self):
        listCameras = cameraChoose.returnCameraIndexes()
        print(f"LISTA DE CAMARAS {listCameras}")

        self.dropDown = DropDown()
        for camera in listCameras:
            print(f"CAMARA {camera}")
            self.button = Button(
                background_color=(255, 255, 255, 0),
                # on_press = lambda x, item=element: print("\nitem number\n", item),
                text=f'CAMARA {camera}',
                size_hint_y=None,
                height=50
            )

            # Ingresando al dropdown
            self.dropDown.add_widget(self.button)
        popUpCamera = self.ids.popUpCamera
        popUpCamera.add_widget(self.dropDown)

    def click(self, item):
        print('holi')








class MenuScreen(Screen):

    '''def update_info(self, username, password):
            self.token = '''

    def prob_tkinter(self):
        tkinter.Label(window, text="Username").grid(row=0)
        tkinter.Entry(window).grid(row=0, column=1)
        tkinter.Label(window, text="Password").grid(row=1)
        tkinter.Entry(window).grid(row=1, column=1)
        tkinter.Checkbutton(window, text="Keep Me Logged In").grid(columnspan=2)
        window.mainloop()

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
                    pos_hint= {"center_x": .5, "center_y": .5}
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
        print(item['ejercicioId']['nombre'])




        self.show = PopUpCamera()
        listCameras = cameraChoose.returnCameraIndexes()
        print(f"LISTA DE CAMARAS {listCameras}")
        self.dropDown = DropDown(
            pos_hint={'center_x': 0.5, 'center_y': 0.8}
        )
        for camera in listCameras:
            print(f"CAMARA {camera}")
            self.button = Button(
                background_color=(255, 0, 255, 0),
                on_press = lambda x, item = camera: self.click_Camera(item),
                text=f'CAMARA {camera}',
                size_hint_y=None,
                height=50
            )

            # Ingresando al dropdown
            self.dropDown.add_widget(self.button)
        self.show.add_widget(self.dropDown)




        popupWindow = Popup(title='Escoge una camara', content=self.show, size_hint=(None, None), size=(400,400))
        popupWindow.open()

        '''MDApp.get_running_app().root.current = 'video'''



    def change_Camera(self, item):
        self.image = Image(
            size_hint= (1, 0.9),
            allow_stretch = True,
            keep_ratio = True,
            post_hint = {'center_x': 0.5, 'top': 1}
        )
        self.show.add_widget(self.image)


    def click_Camera(self, item):
        print(item)





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