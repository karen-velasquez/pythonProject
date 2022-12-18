from kivymd.app import MDApp
import APIRequest as request

#endpoint = 'http://localhost:5000/'
# Inicializando
endpoint = 'http://springbootbackend-env.eba-mmt3kmxg.us-east-1.elasticbeanstalk.com/'
token = ''
class AppAPIRequest():

    def __init__(self):
        pass

    # Redireciona para o dashboard
    def calllogin(self, username, password):
        #Llamando el endpoint
        global endpoint, token
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


def saveCumplimiento(cumplimientoAsignadoChoose):
    global token, endpoint
    cumplimientoObject = request.guardarCumplimiento(token, endpoint, cumplimientoAsignadoChoose)
    return cumplimientoObject









    #Funcion para obtener el token para conectarnos
    def callbackregister(self, *args):
        MDApp.get_running_app().root.current = 'login'




