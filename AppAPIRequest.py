from kivymd.app import MDApp
import APIRequest as request

endpoint = 'http://localhost:5000/'
# Inicializando
#endpoint = 'http://sistemafisioterapiabackend-env.eba-5tweru88.us-east-1.elasticbeanstalk.com/'

class AppAPIRequest():

    def __init__(self):
        pass

    # Redireciona para o dashboard
    def calllogin(self, username, password):
        #Llamando el endpoint
        global endpoint
        token = request.APIRequest.gettoken(self, username, password, endpoint)
        return token



    def calllist(self, token, username):
        # Llamando el endpoint
        global endpoint
        #Imprimiendo el token
        print(token)
        #Imprimiendo la lista de ejercicios
        listaEjercicios = request.APIRequest.listarAsignados(self, token, username, endpoint)
        print(" Y LOS VALORES ")
        print(listaEjercicios)
        return listaEjercicios



    def createPlotAverage(self, token):
        pass




    #Funcion para obtener el token para conectarnos
    def callbackregister(self, *args):
        MDApp.get_running_app().root.current = 'login'




