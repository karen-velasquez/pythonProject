from tkinter import Canvas

from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRectangleFlatButton, MDRoundFlatButton
from kivymd.uix.card import MDCard
import threading
import json
from kivy.graphics import Rectangle, Color

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel

import AppAPIRequest as function
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
#import uix components
from kivy.uix.image import Image, AsyncImage
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.uix.carousel import Carousel

import cv2
import threading
from functools import partial
'''Importando el modulo para que ejercicio se esta llamando'''
import CaseExercise as caseExercise
import CameraChoose as cameraChoose
#import other kivy stuff
from kivy.clock import Clock
from kivy.uix.popup import Popup
from datetime import date

''' Librerias para el informa de Matplolib '''
import ModuleMatplotlib as moduleMatplotlib
import time

'''----------------------------'''

usernameglobal = ''
#Guardando el token en una variable para luego realizar las peticiones
token = ''
#El ejercicio a realizar
ejercicio = 'Flexion codo'
tipo = 'fortalecimiento'
parte = 'superior'
amount = 2
serie = 1
asignadoChoose = {}

#La variable global de la camara
camera = 2



'''--------------------------- AQUI SE CONFIGURA UN MENSAJE DE ALERTA PARA EL INGRESO -------------------------------------------------------'''
class PopUpDescripcion(Popup):
    def __init__(self, item):
        super(PopUpDescripcion, self).__init__()

        # Creando el Content que tendra el PopUp
        content = AnchorLayout(anchor_x='center', anchor_y='bottom')

        #Creando un box Layout que contenga a todos los layouts
        boxlayoutContentComplete = BoxLayout(width=60, orientation='vertical')

        #****** Creando el text que diga deslizar ***********
        boxLayoutContentText = BoxLayout(orientation='vertical', size_hint_y=None)
        contentText = MDLabel(
            text= "Desliza -->",
            font_name= "styles/Poppins-SemiBold.ttf",
            font_size= "15sp",
            halign = 'center',
            theme_text_color= "Custom",
            text_color= (60/255, 43/255, 117/255, 1),
            size_hint_y=None
        )
        boxLayoutContentText.add_widget(contentText)
        boxlayoutContentComplete.add_widget(boxLayoutContentText)
        # ****** Finaliza: Creando el text que diga deslizar ***********



        # ****** Creando el carousel que tendra la informacion ***********
        boxLayoutContentCarousel = BoxLayout(width=60, orientation='vertical',size=(Window.width / 1.1, Window.height / 1.1))
        carousel = Carousel()
        #++++++++++++++++++++ Creando el card de Informacion de ejercicio +++++++++++++++++++++++++
        boxLayoutCardInformation = BoxLayout(width=60, orientation='vertical', size=(Window.width / 1.1, Window.height / 1.1))
        description = MDLabel(
            text=str(item['ejercicioId']['nombre']+"\n"+item['ejercicioId']['descripcion']),
            halign="center",
            font_name="styles/Poppins-SemiBold.ttf",
            font_size="10sp",
            theme_text_color="Custom",
            size_hint_y=None,
            text_color=(60 / 255, 43 / 255, 117 / 255, 1))
        boxLayoutCardInformation.add_widget(description)
        descriptionImage = AsyncImage(
            source=str(item['ejercicioId']['linkImagenFinal']),
            width=60
        )

        boxLayoutCardInformation.add_widget(descriptionImage)
        mdcard = MDCard(
            size_hint=(1, 1),
            width=50,
            pos_hint={"center_x": .5, "center_y": .5}
        )
        # Ingresando la el boton dentro de la imagen y la imagen dentro del card
        # luego agregando el card al carousel
        mdcard.add_widget(boxLayoutCardInformation)
        # ++++++++++++++++++++ Finaliza: Creando el card de Informacion de ejercicio +++++++++++++++++++++++++
        carousel.add_widget(mdcard)
        boxLayoutContentCarousel.add_widget(carousel)
        boxlayoutContentComplete.add_widget(boxLayoutContentCarousel)
        # ****** Finaliza: Creando el carousel que tendra la informacion ***********




        # ++++++++++++++ Creando el boton de OK que lo ayudara a salir +++++++++++++
        ok_button = MDRoundFlatButton(text='Ok', size_hint=(0.5, None), size=(Window.width / 8, Window.height / 15),
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5})
        boxlayoutContentComplete.add_widget(ok_button)
        # ++++++++++++++ Finaliza: Creando el boton de OK que lo ayudara a salir +++++++++++++

        # ***********************************Adicionando el Boxlayout Content Complete al PopUp ****************************
        content.add_widget(boxlayoutContentComplete)
        # *********************************** Creando el Pop Up ****************************
        self.popup = Popup(
            title='ESCOGE UNA DE LAS CAMARAS',
            content=content,
            size_hint=(None, None),
            title_color=(0, 0, 0, 1),
            title_font="styles/Poppins-Regular.ttf",
            title_size='30sp',
            size=(Window.width / 2, Window.height / 1.5),
            auto_dismiss=False,
            background="images/lightBlue.jpg"
        )
        # Dandole la funcion de salir del pop up
        ok_button.bind(on_press=self.popup.dismiss)
        self.popup.open()

'''--------------------------- FINALIZA: AQUI SE CONFIGURA UN MENSAJE DE ALERTA PARA EL INGRESO -------------------------------------------------------'''












'''---------------------------------------- Creando el Pop-Up de la Camara ------------------------------------------------------'''
class PopUpCamera(Popup):

    def __init__(self):
        super(PopUpCamera, self).__init__()

        #Creando el Content que tendra el PopUp
        content = AnchorLayout(anchor_x='center', anchor_y='bottom')

        boxlayoutContentComplete = BoxLayout(width=60, orientation = 'vertical')

        #Creando el boxLayout que ira en el Content
        boxLayoutContent = BoxLayout(width=60, orientation = 'horizontal')

        #***********************************Creando el boxlayout de los Botones****************************
        boxLayoutButtons = BoxLayout(size_hint_x = .3, orientation = 'vertical',padding= 8, spacing= 20)
        #Obteniendo la lista de camaras disponibles
        listCameras = cameraChoose.returnCameraIndexes()
        #Colocando los botones en una caja
        for i in range((len(listCameras)-1)):
        #for camera in listCameras:
            button = MDRoundFlatButton(
                text=f'  CAMARA {listCameras[i]}  ',
                md_bg_color=(0.02, 0.35, 0.42, 0.69),
                font_name="styles/Poppins-SemiBold.ttf",
                text_color="white",
                # on_press = lambda x, item=element: print("\nitem number\n", item),
                on_press =lambda x, item=listCameras[i]: self.click_camera(item),
                size=(Window.width/2, Window.height/10)
            )
            #Adicionando los buttons al box layout
            boxLayoutButtons.add_widget(button)
        widgetExtra = Widget()
        boxLayoutButtons.add_widget(widgetExtra)
        #Adicionando el box al content
        boxLayoutContent.add_widget(boxLayoutButtons)

        # *********************************** Creando el boxlayout de la Imagen ****************************
        boxLayoutImage = BoxLayout(size_hint_x = .7 , orientation = 'vertical')


        self.imageVideo = Image(
            size_hint = (1 , 1),
            allow_stretch = True # allow the video image to be scaled
        )
        boxLayoutImage.add_widget(self.imageVideo)
        boxLayoutContent.add_widget(boxLayoutImage)

        boxlayoutContentComplete.add_widget(boxLayoutContent)

        # *********************************** Creando el boton del salida ****************************
        ok_button = MDRoundFlatButton(text='Ok',
                                      size_hint=(0.5, None),
                                      size=(Window.width / 8, Window.height / 15),
                                      md_bg_color=(0, 0.12, 0.14, 0.69),
                                      font_name="styles/Poppins-SemiBold.ttf",
                                      text_color="white",
                                      pos_hint= {'center_x':0.5, 'center_y':0.5})
        boxlayoutContentComplete.add_widget(ok_button)

        # ***********************************Adicionando el Boxlayout Content Complete al PopUp ****************************
        content.add_widget(boxlayoutContentComplete)

        # *********************************** Creando el Pop Up ****************************
        self.popup = Popup(
            title='ESCOGE UNA DE LAS CÁMARAS',
            content=content,
            size_hint=(None, None),
            title_color = (0,0,0,1),
            title_font = "styles/Poppins-Regular.ttf",
            title_size = '30sp',
            size=(Window.width / 3, Window.height / 2),
            auto_dismiss=False,
            background="images/lightBlue.jpg"
        )
        # Dandole la funcion de salir del pop up
        ok_button.bind(on_press=self.clickVideoClose)
        self.popup.open()
        threading.Thread(target=self.runThreadCamera, daemon=True).start()



    #Cuando se escoja una de las camaras aqui se mostrara el codigo
    def click_camera(self, item):
        time.sleep(0.5)
        global camera
        camera = item
        # stop the video capture loop
        self.stopThreadCamera()
        if (self.cameraFlag == False):
            threading.Thread(target=self.runThreadCamera, daemon=True).start()
            print(f"Este es el item: {camera}")


    #funcion la correr la camara desde un hilo
    def runThreadCamera(self):
        global camera
        # this code is run in a separate thread
        self.cameraFlag = True  # flag to stop loop
        cam = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
        # start processing loop
        while (self.cameraFlag):
            ret, frame = cam.read()
            Clock.schedule_once(partial(self.displayFrameThreadCamera, frame))
        cam.release()
        cv2.destroyAllWindows()

    #Colocando la imagen obtenida por Camara en la imagen que aparecera
    def displayFrameThreadCamera(self, frame, dt):
        # display the current video frame in the kivy Image widget
        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        # copy the frame data into the texture
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')
        # flip the texture (otherwise the video is upside down
        texture.flip_vertical()
        # actually put the texture in the kivy Image widget
        self.imageVideo.texture = texture


    #Funcion para parar el HILO de Camara
    def stopThreadCamera(self):
        # stop the video capture loop
        self.cameraFlag = False
        time.sleep(0.5)


    #Cerrando el popUp
    def clickVideoClose(self, instance):
        self.stopThreadCamera()
        self.popup.dismiss(self)


'''---------------------------------------- FINALIZA: Creando el Pop-Up de la Camara ------------------------------------------------------'''





'''--------------------------- AQUI SE CONFIGURA UN MENSAJE DE ALERTA PARA EL INGRESO -------------------------------------------------------'''
class Alert(Popup):
    def __init__(self, title, text):
        super(Alert, self).__init__()
        content = AnchorLayout(anchor_x='center', anchor_y='bottom')
        content.add_widget(
            Label(text=text, halign='center', valign='top', font_size= "25sp")
        )
        ok_button = Button(text='Ok', size_hint=(None, None), size=(Window.width / 8, Window.height / 15))
        content.add_widget(ok_button)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(None, None),
            size=(Window.width / 2, Window.height / 2),
            auto_dismiss=True,
        )
        ok_button.bind(on_press=popup.dismiss)
        popup.open()
'''--------------------------- FINALIZA: AQUI SE CONFIGURA UN MENSAJE DE ALERTA PARA EL INGRESO -------------------------------------------------------'''




'''--------------------------- AQUI SE CONFIGURA EL MENU SCREEN EN EL QUE SE ENCUENTRA EL LOGIN  -------------------------------------------------------'''
class MenuScreen(Screen):
    def resetInformation(self):
        pass


    #----------Funcion que es llamada cuando se ingresa al print
    def login(self, username, password):
        #Llamando a las variables globales
        global usernameglobal
        global token
        token = ''

        print('el print')

        #Llamando a la función para comprobar que el usuario existe en la BDD
        if(username != '' and password != ''):
            self.resetInformation()
            #guardando el token
            username = username.strip()
            #Corroborando el username y password en la BDD
            token = function.AppAPIRequest.calllogin(self, username, password)
            if token != 500 and token != 0 and token != '':
                MDApp.get_running_app().root.current = 'listExercise'
            else:
                Alert(title='ERROR!!!', text='Hubo problemas en\n la autenticacion!!!')

            #En caso de que el token sea distinto de cadena
            if(token!=''):
                usernameglobal = username

            print(username + '----' + password)
        else:
            Alert(title='ERROR!!!', text='Por favor llenar las casillas!!!')

'''--------------------------- FINALIZA: AQUI SE CONFIGURA EL MENU SCREEN EN EL QUE SE ENCUENTRA EL LOGIN  -------------------------------------------------------'''






'''--------------------------- AQUI SE CONFIGURA EL SCREEN DE VIDEO QUE HACE LAS CORRECIONES A LA PERSONA ---------------------------------------------------'''
class VideoScreen(Screen):
    def on_enter(self):
        #en este treading hacer lo del switch tambie, osea que al escoger tren inferior o algo active el threading de
        # self.parte inferior fortalecimiento o algo asi
        if parte == 'superior' and tipo == 'fortalecimiento':
            threading.Thread(target=self.doSuperiorFort, daemon=True).start()

        elif parte == 'inferior' and tipo == 'fortalecimiento':
            threading.Thread(target=self.doInferiorFort, daemon=True).start()


    #En caso de que el ejercicio escogido sea del Tren superior y de Fortalecimiento
    def doSuperiorFort(self, *args):
        global camera
        # this code is run in a separate thread
        self.do_vid = True  # flag to stop loop
        self.cam = cv2.VideoCapture(camera)

        while (self.do_vid):
            global ejercicio, serie, amount, asignadoChoose
            ret, frame = self.cam.read()

            frame = caseExercise.switch_superior_fortalecimiento(frame, ejercicio, amount, serie, asignadoChoose)
            # the partial function just says to call the specified method with the provided argument (Clock adds a time argument)
            Clock.schedule_once(partial(self.display_frame, frame))

            #cv2.imshow('Hidden', frame)
            #cv2.waitKey(1)
        self.cam.release()
        cv2.destroyAllWindows()

    # En caso de que el ejercicio escogido sea del Tren inferior y de Fortalecimiento
    def doInferiorFort(self, *args):
        global camera
        # this code is run in a separate thread
        self.do_vid = True  # flag to stop loop
        self.cam = cv2.VideoCapture(camera)

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

'''--------------------------- FINALIZA:  AQUI SE CONFIGURA EL SCREEN DE VIDEO QUE HACE LAS CORRECIONES A LA PERSONA ---------------------------------------------------'''



'''---------------------------------- AQUI SE CONFIGURA LA PANTALLA DONDE SE ENCUENTRA LA LISTA DE EJERCICIOS -----------------------------------------'''
class ListExerciseScreen(Screen):
    #*********************************** Al ingresar se carga la lista de ejercicios del usuario******************************************
    def on_enter(self):
        global usernameglobal, token

        #OBTENIENDO LA LISTA DE EJERCICIOS
        listaEjercicios = function.AppAPIRequest.calllist(self, token, usernameglobal)

        # verificando que la lista este llena
        if listaEjercicios != 500 and listaEjercicios != 0 and listaEjercicios != '':
            for element in listaEjercicios:  # iteramos sobre data
                #Creando un boton, que abarcara toda la imagen, cuando se haga click en la imagen el
                #boton activar el self.click

                # Creando un box Layout que contenga a todos los layouts
                boxlayoutContentComplete = BoxLayout(orientation='vertical')

                #Creando el box layout que contendra el texto
                boxLayoutContentText = BoxLayout(orientation='vertical', size_hint_y=None, pos_hint={"center_y": 1})
                #Obteniendo el texto que estara
                asignadoTitle = f"\n\n\n\n[b][size=24]{element['ejercicioId']['nombre']}[/size][/b] \n\n"
                asignadoText = f"\n\n\n[b]Series:[/b]     {element['series']} \n"+\
                               f"[b]Repeticiones:[/b]     {element['repeticiones']} \n"+\
                               f"[b]Hasta:[/b]     {element['fechafinalizacion']} \n"

                contentTitle = MDLabel(
                    text=asignadoTitle,
                    font_name="styles/Poppins-SemiBold.ttf",
                    font_size="15sp",
                    halign='center',
                    pos_hint={"center_y": .8},
                    theme_text_color="Custom",
                    text_color=(60 / 255, 43 / 255, 117 / 255, 1),
                    markup=True
                )
                contentText = MDLabel(
                    text=asignadoText,
                    font_name="styles/Poppins-SemiBold.ttf",
                    font_size="15sp",
                    halign='left',
                    theme_text_color="Custom",
                    text_color=(60 / 255, 43 / 255, 117 / 255, 1),
                    size_hint_y=None,
                    pos_hint={"center_x": .7},
                    markup=True
                )
                boxLayoutContentText.add_widget(contentTitle)
                boxLayoutContentText.add_widget(contentText)
                boxlayoutContentComplete.add_widget(boxLayoutContentText)


                #Creando Box Layout que contenga la imagen
                boxLayoutContentImage = BoxLayout(orientation='vertical', padding= 10)
                asyncImage = AsyncImage(
                    source=str(element['ejercicioId']['linkImagenFinal']),
                    #height=90,
                    #size= (self.width + 20, self.height + 20)
                )
                # Ingresando la el boton dentro de la imagen y la imagen dentro del card
                # luego agregando el card al carousel
                boxLayoutContentImage.add_widget(asyncImage)
                boxlayoutContentComplete.add_widget(boxLayoutContentImage)

                # Creando Box Layout el boton
                button = MDRoundFlatButton(
                    text= "REALIZA ESTE EJERCICIO!!!",
                    font_name="styles/Poppins-SemiBold.ttf",
                    text_color= "white",
                    md_bg_color= (0.33, 0.72, 0.76, 0.8),
                    size_hint_y=None,
                    pos_hint={"center_x": .5},
                    padding = 15,
                    on_press = lambda x, item = element: self.click(item)
                )
                boxlayoutContentComplete.add_widget(button)


                #Creando el Card
                mdcard = MDCard(
                    size_hint= (.4, .8),
                    pos_hint= {"center_x": .5, "center_y": .5},
                    md_bg_color="#eaf4f4"
                )
                mdcard.add_widget(boxlayoutContentComplete)


                #Obteniendo el box layout e incorporando el carousel
                carousel=self.ids.carousel
                carousel.add_widget(mdcard)
        else:
            print('Hubo problemas en la autenticacion')

    #Eliminando los objetos que tiene el carousel
    def removeCarousel(self):
        #Limpiando el carousel
        self.ids.carousel.clear_widgets()



    # *********************************** Al hacer click en uno de los ejercicios de carousel ******************************************
    def click(self, itemEjercicio):
        global parte, tipo, ejercicio, asignadoChoose, amount, serie
        parte = itemEjercicio['ejercicioId']['parteCuerpo']
        tipo = itemEjercicio['ejercicioId']['tipo']
        ejercicio = itemEjercicio['ejercicioId']['nombre']
        amount = int(itemEjercicio['repeticiones'])
        serie = int(itemEjercicio['series'])

        #Configurando el objeto de Cumplimiento para enviarlo
        #Llamando la fechad de hoy
        today = date.today()
        json_data = {
            'fechaCumplimiento':today.strftime("%Y-%m-%d"),
            "asignadoId": {
                "asignadoId": itemEjercicio['asignadoId']},
            'aciertos': 0,
            'serieRealizada': 3}
        asignadoChoose = json_data
        #Finaliza: Configurando el objeto de Cumplimiento para enviarlo

        #PopUpDescripcion(item = itemEjercicio)
        MDApp.get_running_app().root.current = 'video'



    # ************************************* FUNCIONES DE LOS BOTONES *********************************************************
    #+++++++++++++++++++++++++++++++++ CAMERA +++++++++++++++++++++++++++
    def btnCamara(self):
        #Creando un hilo que abrirá la cámara

        self.crearPopUpCamera()

    def crearPopUpCamera(self):
        PopUpCamera()




    # +++++++++++++++++++++++++++++++++ INFORME +++++++++++++++++++++++++++
    #Cuando se hace click en el informe de ejercicios
    def btnInformeEjercicios(self):
        #Creando un hilo que cree el grafico
        threading.Thread(target=self.informeEjercicios, args=()).start()

    # HILO: para crear el grafico de ejercicios
    def informeEjercicios(self):
        global usernameglobal, token
        moduleMatplotlib.plotEjercicios(usernameglobal, token)



    # +++++++++++++++++++++++++++++++++ EXTRA INFORMATION +++++++++++++++++++++++++++
    def btnInformacion(self):
        pass






'''---------------------------------- FINALIZA: AQUI SE CONFIGURA LA PANTALLA DONDE SE ENCUENTRA LA LISTA DE EJERCICIOS -----------------------------------------'''




'''----------------------  CREANDO EL SCREENMANAGER E ADICIONANDO LOS SCREENS A CONTROLAR  -----------------------------------'''
# Create the screen manager
sm = ScreenManager()
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(VideoScreen(name='video'))
sm.add_widget(ListExerciseScreen(name='listExercise'))
'''----------------------  FINALIZA: CREANDO EL SCREENMANAGER E ADICIONANDO LOS SCREENS A CONTROLAR  -----------------------------------'''




''' ----------------------------------------  CONFIGURANDO LA PANTALLA PRINCIPAL  --------------------------------------------'''
class DemoApp(MDApp):
    def build(self):
        screen = Builder.load_file('ScreensApp.kv')
        return screen
''' ---------------------------------------- FINALIZA: CONFIGURANDO LA PANTALLA PRINCIPAL  --------------------------------------------'''


#Inicializando la DemoApp()
DemoApp().run()