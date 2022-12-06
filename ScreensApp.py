from kivy.uix.dropdown import DropDown
from kivy.uix.floatlayout import FloatLayout
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.card import MDCard

from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel

import AppAPIRequest as function
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import  Layout
#import uix components
from kivy.uix.image import Image, AsyncImage
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.uix.carousel import Carousel
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


''' Librerias para el informa de Matplolib '''
import ModuleMatplotlib as moduleMatplotlib

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



'''--------------------------- AQUI SE CONFIGURA UN MENSAJE DE ALERTA PARA EL INGRESO -------------------------------------------------------'''
class PopUpDescripcion(Popup):
    def __init__(self, item):
        super(PopUpDescripcion, self).__init__()



        # Creando el Content que tendra el PopUp
        content = AnchorLayout(anchor_x='center', anchor_y='bottom')

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
        carousel.add_widget(mdcard)

        boxLayoutContentCarousel.add_widget(carousel)
        boxlayoutContentComplete.add_widget(boxLayoutContentCarousel)
        # ++++++++++++++++++++ Finaliza: Creando el card de Informacion de ejercicio +++++++++++++++++++++++++



        ok_button = Button(text='Ok', size_hint=(0.5, None), size=(Window.width / 8, Window.height / 15),
                                        pos_hint={'center_x': 0.5, 'center_y': 0.5})
        boxlayoutContentComplete.add_widget(ok_button)
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




        '''#++++++++++++++++++++ Creando el card de Informacion de ejercicio +++++++++++++++++++++++++
        self.asyncImage = AsyncImage(
            source=str(item['ejercicioId']['linkImagenFinal']),
            pos=self.parent.pos,
            size=self.parent.size
        )
        self.mdcard = MDCard(
            size_hint=(.6, .6),
            pos_hint={"center_x": .5, "center_y": .5}
        )
        # Ingresando la el boton dentro de la imagen y la imagen dentro del card
        # luego agregando el card al carousel
        self.asyncImage.add_widget(self.button)
        self.mdcard.add_widget(self.asyncImage)
        # ++++++++++++++++++++ Finaliza: Creando el card de Informacion de ejercicio +++++++++++++++++++++++++


        carousel.add_widget(self.mdcard)
        # *********************************** Creando el boton del salida ****************************
        '''
        '''ok_button = Button(text='Ok', size_hint=(0.5, None), size=(Window.width / 8, Window.height / 15),
                                pos_hint={'center_x': 0.5, 'center_y': 0.5})
        boxlayoutContentComplete.add_widget(self.ok_button)

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
            size=(Window.width / 2, Window.height / 2),
            auto_dismiss=False,
            background="images/lightBlue.jpg"
        )
        # Dandole la funcion de salir del pop up
        ok_button.bind(on_press=self.clickVideoClose)
        self.popup.open()'''










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
        for camera in listCameras:
            button = Button(
                text=f'CAMARA {camera}',
                background_normal= '',
                background_color= (.70, .83, .89, 1),
                # on_press = lambda x, item=element: print("\nitem number\n", item),
                on_press =lambda x, item=camera: self.click_camera(item),
                size=(Window.width / 8, Window.height / 15)
            )
            #Adicionando los buttons al box layout
            boxLayoutButtons.add_widget(button)
        widgetExtra = Widget()
        boxLayoutButtons.add_widget(widgetExtra)
        #Adicionando el box al content
        boxLayoutContent.add_widget(boxLayoutButtons)

        # *********************************** Creando el boxlayout de la Imagen ****************************
        boxLayoutImage = BoxLayout(size_hint_x = .7 , orientation = 'vertical')
        imageVideo = Image(
            size_hint = (1 , 1),
            allow_stretch = True,  # allow the video image to be scaled
            source= "images/logo_fisio.jpg"
        )
        boxLayoutImage.add_widget(imageVideo)
        boxLayoutContent.add_widget(boxLayoutImage)

        boxlayoutContentComplete.add_widget(boxLayoutContent)

        # *********************************** Creando el boton del salida ****************************
        ok_button = Button(text='Ok', size_hint=(0.5, None), size=(Window.width / 8, Window.height / 15),pos_hint= {'center_x':0.5, 'center_y':0.5})
        boxlayoutContentComplete.add_widget(ok_button)

        # ***********************************Adicionando el Boxlayout Content Complete al PopUp ****************************
        content.add_widget(boxlayoutContentComplete)

        # *********************************** Creando el Pop Up ****************************
        self.popup = Popup(
            title='ESCOGE UNA DE LAS CAMARAS',
            content=content,
            size_hint=(None, None),
            title_color = (0,0,0,1),
            title_font = "styles/Poppins-Regular.ttf",
            title_size = '30sp',
            size=(Window.width / 2, Window.height / 2),
            auto_dismiss=False,
            background="images/lightBlue.jpg"
        )
        # Dandole la funcion de salir del pop up
        ok_button.bind(on_press=self.clickVideoClose)
        self.popup.open()



    def click_camera(self, item):
        print(f"Este es el item: {item}")

    def clickVideoClose(self, instance):
        self.popup.dismiss(self)
        print("holiiiiiiiiiiiiiii ")
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


    def login(self, username, password):
        print('el print')
        #print(MDApp.get_running_app().root.manager.MY_GLOBAL)
        global usernameglobal
        global token
        token = ''
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

'''--------------------------- FINALIZA:  AQUI SE CONFIGURA EL SCREEN DE VIDEO QUE HACE LAS CORRECIONES A LA PERSONA ---------------------------------------------------'''



'''---------------------------------- AQUI SE CONFIGURA LA PANTALLA DONDE SE ENCUENTRA LA LISTA DE EJERCICIOS -----------------------------------------'''
class ListExerciseScreen(Screen):

    #*********************************** Al ingresar se carga la lista de ejercicios del usuario******************************************
    def on_enter(self):
        global usernameglobal, token
        listaEjercicios = function.AppAPIRequest.calllist(self, token, usernameglobal)
        # verificando que la lista este llena
        if listaEjercicios != 500 and listaEjercicios != 0 and listaEjercicios != '':
            for element in listaEjercicios:  # iteramos sobre data
                print("----------------------- ELEMENTO ------------------------------------")
                print(element)

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

    # *********************************** Al hacer click en uno de los ejercicios de carousel ******************************************
    def click(self, itemEjercicio):
        global parte, tipo, ejercicio
        parte = itemEjercicio['ejercicioId']['parteCuerpo']
        tipo = itemEjercicio['ejercicioId']['tipo']
        ejercicio = itemEjercicio['ejercicioId']['nombre']
        print('--------------EL TIPO DE ITEM----------')
        print(itemEjercicio)

        PopUpDescripcion(item = itemEjercicio)
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



    # ************************************* FUNCIONES DE LOS BOTONES *********************************************************
    def btnInforme(self):
        global token, usernameglobal
        print("EL TOKEN    "+token)
        print(" El usuario global: "+usernameglobal)
        json_str = '[{"Fee":"80","Duration":"1-10-2022","Discount":"80"},\
                {"Fee":"90","Duration":"2-10-2022","Discount":"69.9"},\
                {"Fee":"90","Duration":"3-10-2022","Discount":"85"}, \
                {"Fee":"80","Duration":"1-11-2022","Discount":"88"},\
                {"Fee":"70","Duration":"2-11-2022","Discount":"90.2"},\
                {"Fee":"90","Duration":"3-11-2022","Discount":"100"}, \
                {"Fee":"70","Duration":"1-09-2022","Discount":"60"},\
                {"Fee":"69","Duration":"2-09-2022","Discount":"61.2"},\
                {"Fee":"70","Duration":"3-09-2022","Discount":"50.0"}, \
                {"Fee":NaN,"Duration":"4-10-2022","Discount":"80"},\
                {"Fee":"90","Duration":"5-10-2022","Discount":"69.9"},\
                {"Fee":"80","Duration":"6-10-2022","Discount":"85"}, \
                {"Fee":NaN,"Duration":"7-11-2022","Discount":"88"},\
                {"Fee":"80","Duration":"8-11-2022","Discount":"90.2"},\
                {"Fee":NaN,"Duration":"9-11-2022","Discount":"100"}, \
                {"Fee":NaN,"Duration":"10-09-2022","Discount":"60"},\
                {"Fee":"80","Duration":"11-09-2022","Discount":"61.2"}]'
        moduleMatplotlib.plot(json_str)

    def btnInformeEjercicios(self):
        global usernameglobal, token
        moduleMatplotlib.plotEjercicios(usernameglobal, token)



    def btnCamara(self):
        PopUpCamera()
        pass


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