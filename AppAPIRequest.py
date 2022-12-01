from kivymd.app import MDApp
import APIRequest as request

# Inicializando
endpoint = 'http://sistemafisioterapiabackend-env.eba-5tweru88.us-east-1.elasticbeanstalk.com/'
token = ''
listaEjercicios = ''
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
        global listaEjercicios
        #Imprimiendo el token
        print(token)
        #Imprimiendo la lista de ejercicios
        listaEjercicios = request.APIRequest.listarAsignados(self, token, username, endpoint)
        return listaEjercicios




    #Funcion para obtener el token para conectarnos
    def callbackregister(self, *args):
        MDApp.get_running_app().root.current = 'login'




