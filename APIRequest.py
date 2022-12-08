import time

import requests  #Importamos la librería requests


class APIRequest():
    #Inicializando
    def __init__(self):
        pass

    #Funcion para obtener el token para conectarnos
    def gettoken(self, username, password, endpoint):
        #Realizando el token
        request = requests.post(endpoint+'generate-token',
                          json={
                              "username": str(username),
                              "password": str(password)
                          })

        if (request.status_code == 200):
            # Obteniendo el data del request
            data = request.json()
            token = data['token']
            return token
        else:
            if (request.status_code == 500):
                return 500
            else:
                if (request.status_code == 0):
                    return 0

    def listarAsignados(self, token, username, end_point):
        #definiendo el header
        headers = {"Authorization": "Bearer " + str(token)}
        #creando el request
        request = requests.get(str(end_point)+"asignado/paciente/"+str(username), headers=headers)

        #obteniendo la data
        data = request.json()

        if (request.status_code == 200):
            # Obteniendo el data del request
            return data
        else:
            if (request.status_code == 500):
                return 'Hubo un error al pedir los datos'
            else:
                if (request.status_code == 0):
                    return 'No hay conexion con el servidor'




def guardarCumplimiento(token, end_point, cumplimientoObject):
    # definiendo el header
    headers = {"Authorization": "Bearer " + str(token)}
    print("llego aqui?---------------")
    # creando el request
    request = requests.post(str(end_point)+"cumplimiento/", headers=headers, json=cumplimientoObject)
    #r = requests.post('http://httpbin.org/post', json={"key": "value"})
    # obteniendo la data
    data = request.json()
    if (request.status_code == 200):
        # Obteniendo el data del request
        return data
    else:
        if (request.status_code == 500):
            return 'Hubo un error al pedir los datos'
        else:
            if (request.status_code == 0):
                return 'No hay conexion con el servidor'











'''def main():
    apiRequest = APIRequest()
    apiRequest.gettoken("karen123","123")
    print(apiRequest.listarPacientes())


if __name__ == "__main__":
    main()'''