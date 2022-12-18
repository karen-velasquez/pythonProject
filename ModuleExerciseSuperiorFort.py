import cv2
import numpy as np
import threading
import pyttsx3
import mediapipe as mp
from datetime import datetime
import AppAPIRequest as function
import time
import pygame
language = 'en'

'''++++++++++++++++++++++++++++ EL VALOR DEL TIME: ES LOS VALORES QUE SE USAN PARA EL CONTADOR ENTRE REPETICIONES++++++++++++++++++++++++++++++++++++'''
# Initialize variables
saveCount = 0
nSecond = 0
totalSec = 4
strSec = '4321'
startTime = datetime.now()
timeElapsed = 0.0
startCounter = True
endCounter = False
'''++++++++++++++++++++++++++++ FINALIZA: EL VALOR DEL TIME ++++++++++++++++++++++++++++++++++++'''

'''--------------------- CONFIGURAR LO NECESARIO PARA EL RECONOCIMIENTO DE POSES ------------------------'''
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose_model = mp_pose.Pose(
    static_image_mode=False,
    min_detection_confidence=0.7,
    smooth_landmarks=True,
    min_tracking_confidence=0.7
)
'''--------------------- FINALIZA: CONFIGURAR LO NECESARIO PARA EL RECONOCIMIENTO DE POSES ------------------------'''


'''--------------------------VARIABLES GLOBALES---------------------------'''
#Esto vera el estado si es down o up
#El stage es para ser un flag del tiempo en general
stage = ''
#El stagetwo es un flag de la elevacion en general si esta flexionanado mucho o no
stagetwo = ''

'''-----------------------Contadores del sistema ---------------------------'''
#Esto contara todas las repeticiones del ejercicio
counter = 0
#Esto contara las repeticiones erroneas
wrong_counter = 0
#La series del ejercicio
exercise_serie = 0
#Tiempo entre sesiones-----------
ml = 0
se = 5
dir = 0
#Obteniendo el objeto cumplimiento mediante el cual se guardara los datos
cumplimientoObjectUpdate={}
#flag para enviar el valor a la BDD esto es para que no espere a terminar la serie
cumplimientoflag = 0

#Monto necesario son la cantidad de repeticiones usualmente 12
montoNecesario=0




'''---------------------------- CONFIGURANDO LA VOZ---------------------------------------------------'''
engine = pyttsx3.init()
voices = engine.getProperty('voices')
# verificando que la voz exista ****REVISAR LUEGO*****
number = 2
if (len(voices) == number):
    number = 0
    print('es mayor')
engine.setProperty('voice', voices[number].id)
# controlando el rate, a higuer rate = mas rapido
engine.setProperty('rate', 150)
'''---------------------------- FINALIZA: CONFIGURANDO LA VOZ---------------------------------------------------'''


'''--------------------------FINALIZA: VARIABLES GLOBALES---------------------------'''


'''+++++++++++++++++++++++++++++ DEVUELVE TODOS LOS VALORES A SU ESTADO ORIGINAL +++++++++++++++++++++++++++++++++'''

def returnValuesOriginal():
    global saveCount, nSecond, totalSec, strSec, startTime, timeElapsed, startCounter, endCounter
    #+++++++++++++++++ EL VALOR DEL TIME: ES LOS VALORES QUE SE USAN PARA EL CONTADOR ENTRE REPETICIONES++++++++++++'''
    # Initialize variables
    saveCount = 0
    nSecond = 0
    totalSec = 4
    strSec = '4321'
    startTime = datetime.now()
    timeElapsed = 0.0
    startCounter = True
    endCounter = False
    #++++++++++++++++++++++++++++ FINALIZA: EL VALOR DEL TIME ++++++++++++++++++++++++++++++++++++'''

    #--------------------------VARIABLES GLOBALES---------------------------'''
    global stage, stagetwo
    # Esto vera el estado si es down o up
    # El stage es para ser un flag del tiempo en general
    stage = ''
    # El stagetwo es un flag de la elevacion en general si esta flexionanado mucho o no
    stagetwo = ''

    #-----------------------Contadores del sistema ---------------------------'''
    global counter, wrong_counter, exercise_serie, ml, se, dir, cumplimientoObjectUpdate, cumplimientoflag, montoNecesario
    # Esto contara todas las repeticiones del ejercicio
    counter = 0
    # Esto contara las repeticiones erroneas
    wrong_counter = 0
    # La series del ejercicio
    exercise_serie = 0
    # Tiempo entre sesiones-----------
    ml = 0
    se = 5
    dir = 0
    # Obteniendo el objeto cumplimiento mediante el cual se guardara los datos
    cumplimientoObjectUpdate = {}
    # flag para enviar el valor a la BDD esto es para que no espere a terminar la serie
    cumplimientoflag = 0
    # Monto necesario son la cantidad de repeticiones usualmente 12
    montoNecesario = 0







'''+++++++++++++++++++++++++++++++++++++ FINALIZA: DEVUELVE TODOS LOS VALORES A SU ESTADO ORIGINAL   +++++++++++++++++++++++++++++++++'''



'''---------------------------------------------   POSE PROCESS  ---------------------------------------------------------'''
def poseProcess(frame):
    global mp_pose, pose_model
    # Recolor image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    # Make detection
    results = pose_model.process(image)
    # Recolor back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return results

    return switch(image, mp_pose, results, ejercicio, amount, serie)

'''--------------------------------------------- FINALIZA:  POSE PROCESS  ---------------------------------------------------------'''




'''---------------------------- DIBUJANDO LA IMAGEN QUE SALDRA ---------------------------------------------------'''
'''FUNCION QUE DIBUJA SOBRE EL CV2'''
def draw_cv2(image):
    global counter, stage, wrong_counter
    #Contador general
    cv2.rectangle(image, (202, 0), (265, 50), (102, 51, 0), -1)
    cv2.rectangle(image, (0, 0), (200, 50), (255, 0, 0), -1)
    cv2.rectangle(image, (202, 0), (265, 50), (255, 0, 0), 2)
    cv2.putText(image, "Contador:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(image, "{}".format(counter), (220, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,255,255), 2)

    #Contador de erroneas
    cv2.rectangle(image, (202, 50), (265, 100), (102, 51, 0), -1)
    cv2.rectangle(image, (0, 50), (200, 100), (255, 255, 0), -1)
    cv2.rectangle(image, (202, 50), (265, 100), (255, 255, 0), 2)
    cv2.putText(image, "Erroneas:", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(image, "{}".format(wrong_counter), (220, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

'''---------------------------- FINALIZA: DIBUJANDO LA IMAGEN QUE SALDRA ---------------------------------------------------'''




'''---------------------------- OBTENIENDO LA IMAGEN SOLO DE LOS PUNTOS ---------------------------------------------------'''

#Dibujando solo los puntos y lineas del brazo
def draw_left_arm(results, image):
    global stage, stagetwo
    height, width, _ = image.shape
    x1 = int(results.pose_landmarks.landmark[11].x * width)
    y1 = int(results.pose_landmarks.landmark[11].y * height)
    x2 = int(results.pose_landmarks.landmark[13].x * width)
    y2 = int(results.pose_landmarks.landmark[13].y * height)
    x3 = int(results.pose_landmarks.landmark[15].x * width)
    y3 = int(results.pose_landmarks.landmark[15].y * height)

    color_line = (0, 0, 255)
    color_circle = (0, 0, 255)

    if stage == 'inicial':
        # Confirgurando el color de la linea
        color_line = (255, 255, 255)
        color_circle = (255, 255, 255)

    elif stage == "final" and stagetwo == "inter":
        color_line = (0, 255, 0)
        color_circle = (0, 255, 0)

    elif stage == "final" and stagetwo == "final":
        color_line = (0, 0, 255)
        color_circle = (0, 0, 255)

    else:
        color_line = (255, 0, 0)
        color_circle = (255, 0, 0)

    cv2.line(image, (x1, y1), (x2, y2), color_line, 3)
    cv2.line(image, (x3, y3), (x2, y2), color_line, 3)
    cv2.circle(image, (x1, y1), 10, color_circle, cv2.FILLED)
    cv2.circle(image, (x1, y1), 15, color_circle, 2)
    cv2.circle(image, (x2, y2), 10, color_circle, cv2.FILLED)
    cv2.circle(image, (x2, y2), 15, color_circle, 2)
    cv2.circle(image, (x3, y3), 10, color_circle, cv2.FILLED)
    cv2.circle(image, (x3, y3), 15, color_circle, 2)


def draw_left_hip_arm(results, image):
    height, width, _ = image.shape
    x1 = int(results.pose_landmarks.landmark[23].x * width)
    y1 = int(results.pose_landmarks.landmark[23].y * height)
    x2 = int(results.pose_landmarks.landmark[11].x * width)
    y2 = int(results.pose_landmarks.landmark[11].y * height)
    x3 = int(results.pose_landmarks.landmark[15].x * width)
    y3 = int(results.pose_landmarks.landmark[15].y * height)

    color_line = (0, 0, 255)
    color_circle = (0, 0, 255)

    if stage == 'inicial':
        # Confirgurando el color de la linea
        color_line = (255, 255, 255)
        color_circle = (255, 255, 255)

    elif stage == "final" and stagetwo == "inter":
        color_line = (0, 255, 0)
        color_circle = (0, 255, 0)

    elif stage == "final" and stagetwo == "final":
        color_line = (0, 0, 255)
        color_circle = (0, 0, 255)

    else:
        color_line = (255, 0, 0)
        color_circle = (255, 0, 0)

    cv2.line(image, (x1, y1), (x2, y2), color_line, 3)
    cv2.line(image, (x3, y3), (x2, y2), color_line, 3)
    cv2.circle(image, (x1, y1), 10, color_circle, cv2.FILLED)
    cv2.circle(image, (x1, y1), 15, color_circle, 2)
    cv2.circle(image, (x2, y2), 10, color_circle, cv2.FILLED)
    cv2.circle(image, (x2, y2), 15, color_circle, 2)
    cv2.circle(image, (x3, y3), 10, color_circle, cv2.FILLED)
    cv2.circle(image, (x3, y3), 15, color_circle, 2)






'''---------------------------- FINALIZA: OBTENIENDO LA IMAGEN SOLO DE LOS PUNTOS ---------------------------------------------------'''











'''---------------------------- DIBUJANDO LOS ERRORES ---------------------------------------------------'''
'''FUNCION QUE DIBUJA SOBRE EL CV2'''


def draw_cv2_error(texto_error, image):
    fontScale = 1.4
    thickness = 3
    fontFace = cv2.FONT_HERSHEY_SIMPLEX

    cv2.rectangle(image, (150, 170), (550, 340), (102, 51, 0), -1)

    y0, dy = 220, 50
    for i, line in enumerate(texto_error.split('\n')):
        y = y0 + i * dy
        cv2.putText(image, line, (200, y),fontFace, fontScale, (255, 255, 255), thickness, cv2.LINE_AA)














'''---------------------------- FINALIZA: DIBUJANDO LOS ERRORES ---------------------------------------------------'''






'''---------------------------- DIBUJANDO EL BAR ---------------------------------------------------'''
'''FUNCION QUE DIBUJA SOBRE EL CV2'''
def draw_cv2_bar(angle, maxAngle, minAngle, minLimit, maxLimit, image):
    #Obteniendo los valores globales
    global count, dir, stage
    # Check for the dumbbell curls
    color = (255, 0, 255)



    if stage == 'inicial':
        color = (255,255,255)
        #valor del bar
        bar = np.interp(angle, (minAngle, maxAngle), (minLimit, maxLimit))

        # Draw Bar
        #Rectangulo general
        cv2.rectangle(image, (120, 150), (160, 400), color, 3)
        #Llenando el rectangulo
        cv2.rectangle(image, (120, int(bar)), (160, 400), color, cv2.FILLED)
        # Aumentando un texto que le diga que inicie
        cv2.putText(image, 'INICIA!!!', (100, 450), cv2.FONT_HERSHEY_SIMPLEX,
                            1, color, 2, cv2.LINE_AA)

    elif stage == "final" and stagetwo == "inter":
        color = (0, 255, 0)
        cv2.rectangle(image, (120, 150), (160, 400), color, 3)

    elif stage == "final" and stagetwo == "final":
        color= (0, 0, 255)
        cv2.rectangle(image, (120, 150), (160, 400), color, 3)

    else:
        color = (255, 0, 0)
        cv2.rectangle(image, (120, 150), (160, 400), color, 3)





'''---------------------------- FINALIZA: DIBUJANDO LOS ERRORES ---------------------------------------------------'''















'''---------------------------- CALCULANDO LOS ANGULOS NECESARIOS ---------------------------------------------------'''
#******** Funcion para calcular el angulo entre tres puntos**************
def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle



#**************** CALCULANDO EL ANGULO DEL BRAZO IZQUIERDO ******************************
def leftArmAngle(results, image):
    height, width, _ = image.shape
  
    int(results.pose_landmarks.landmark[11].x * width)
    left_shoulder = [int(results.pose_landmarks.landmark[11].x * width),
                     int(results.pose_landmarks.landmark[11].y * height)]
    left_elbow = [int(results.pose_landmarks.landmark[13].x * width),
                  int(results.pose_landmarks.landmark[13].y * height)]
    left_wrist = [int(results.pose_landmarks.landmark[15].x * width),
                  int(results.pose_landmarks.landmark[15].y * height)]

    threading.Thread(target=draw_left_arm, args=(results, image,)).start()

    return calculate_angle(left_shoulder, left_elbow, left_wrist)



#El calculo del brazo y cadera izquierda
def leftArmHipAngle(results, image):
    height, width, _ = image.shape

    left_hip = [int(results.pose_landmarks.landmark[23].x * width),
                     int(results.pose_landmarks.landmark[23].y * height)]
    left_shoulder = [int(results.pose_landmarks.landmark[11].x * width),
                  int(results.pose_landmarks.landmark[11].y * height)]
    left_wrist = [int(results.pose_landmarks.landmark[15].x * width),
                  int(results.pose_landmarks.landmark[15].y * height)]

    threading.Thread(target=draw_left_hip_arm, args=(results, image,)).start()

    return calculate_angle(left_hip, left_shoulder, left_wrist)





'''---------------------------- FINALIZA: CALCULANDO LOS ANGULOS NECESARIOS ---------------------------------------------------'''

'''-------------------------- ESTOS SON LOS EXTRAS  -----------------------------------------'''
#Convirtiendo el texto en voz
def text_to_speech(feedback):
    engine.say(feedback)
    engine.runAndWait()

#Diciendo bien cuando se realizo el ejericio correctamente
def text_correct_exercise():
    pygame.init()
    pygame.mixer.music.load("bien.mp3")
    pygame.mixer.music.play()
    time.sleep(2)

'''-------------------------- FINALIZA: ESTOS SON LOS EXTRAS  -----------------------------------------'''




'''---------------------------- FEEDBACK DE LOS EJERCICIOS - FORTALECIMIENTO - TREN INFERIOR ---------------------------------------------------'''

#Ejercicio de flexion de codo
def flexionCodo(results, image):
    #Ingresando al global stage para modificarlo
    global stage, stagetwo, counter, wrong_counter

    #Verificando que se vean los puntos del brazo
    if (results.pose_landmarks.landmark[13].visibility > 0.90 and results.pose_landmarks.landmark[15].visibility > 0.90):
        left_arm_angle = leftArmAngle(results, image,)

        #HILO: Creando el draw bar
        threading.Thread(target=draw_cv2_bar, args=(left_arm_angle,160,90,150,400,image,)).start()

        #Si el angulo es mayor a 160 entonces se encuentra en la posicion inicial
        if left_arm_angle > 160:
            stage = "inicial"

        '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
        global startCounter, nSecond, totalSec, timeElapsed, saveCount, startTime
        if stage == "inicial":
            if startCounter:
                if nSecond < totalSec:
                    # draw the Nth second on each frame
                    cv2.circle(image, (510, 420), 60, (255, 0, 0), -1)
                    cv2.putText(image, strSec[nSecond], (480, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5,
                                cv2.LINE_AA)  # adding timer text

                    timeElapsed = (datetime.now() - startTime).total_seconds()

                    if timeElapsed >= 1:
                        nSecond += 1
                        timeElapsed = 0
                        startTime = datetime.now()

                else:
                    saveCount += 1
                    startCounter = False
                    nSecond = 0
        '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''

        if left_arm_angle > 80 and left_arm_angle < 90 and stage == "inicial":
            if nSecond>0:
                stage = 'final'
                stagetwo = 'final'
                wrong_counter = wrong_counter + 1
                counter = counter + 1
                feedback = 'muy rapido'
                #HILO: Informando del error de tiempo : muy rapido!!!
                threading.Thread(target=text_to_speech, args=(feedback,)).start()

                '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
                startCounter = True
                startTime = datetime.now()
                nSecond = 0
                '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''

            else:
                stage = "final"
                stagetwo = 'inter'
                counter = counter + 1
                #HILO: Contabilizando la cantidad de repeticiones
                threading.Thread(target=text_correct_exercise, args=()).start()

                '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
                startCounter = True
                startTime = datetime.now()
                nSecond = 0
                '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''

        elif left_arm_angle < 70 and stagetwo=="inter":
            stage = "final"
            stagetwo = "final"
            feedback = "Flexionas mucho tu brazo"
            wrong_counter = wrong_counter + 1
            #Informando del error de flexion
            threading.Thread(target=text_to_speech, args=(feedback,)).start()

            '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
            startCounter = True
            startTime = datetime.now()
            nSecond = 0

    else:
        feedback = '  NO SE VE\n  TU BRAZO'
        #HILO: Creando el hilo que indica si se ven los puntos necesarios para el analisis
        threading.Thread(target=draw_cv2_error, args=(feedback, image,)).start()








#Ejercicio de flexion de hombro
def flexionHombro(results, image):
    #Ingresando al global stage para modificarlo
    global stage, stagetwo, counter, wrong_counter

    #Verificando que se vean los puntos del brazo
    if (results.pose_landmarks.landmark[15].visibility > 0.90 and results.pose_landmarks.landmark[23].visibility > 0.90):


        left_arm_hip_angle = leftArmHipAngle(results, image, )


        #HILO: Creando el draw bar
        threading.Thread(target=draw_cv2_bar, args=(left_arm_hip_angle,85,10,400, 150,image,)).start()

        #Si el angulo es mayor a 160 entonces se encuentra en la posicion inicial
        if left_arm_hip_angle < 15:
            stage = "inicial"

        '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
        global startCounter, nSecond, totalSec, timeElapsed, saveCount, startTime
        if stage == "inicial":
            if startCounter:
                if nSecond < totalSec:
                    # draw the Nth second on each frame
                    cv2.circle(image, (510, 420), 60, (255, 0, 0), -1)
                    cv2.putText(image, strSec[nSecond], (480, 450), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 5,
                                cv2.LINE_AA)  # adding timer text

                    timeElapsed = (datetime.now() - startTime).total_seconds()

                    if timeElapsed >= 1:
                        nSecond += 1
                        timeElapsed = 0
                        startTime = datetime.now()

                else:
                    saveCount += 1
                    startCounter = False
                    nSecond = 0
        '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''

        if left_arm_hip_angle > 75 and left_arm_hip_angle < 85 and stage == "inicial":
            if nSecond>0:
                stage = 'final'
                stagetwo = 'final'
                wrong_counter = wrong_counter + 1
                counter = counter + 1
                feedback = 'muy rapido'
                #HILO: Informando del error de tiempo : muy rapido!!!
                threading.Thread(target=text_to_speech, args=(feedback,)).start()

                '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
                startCounter = True
                startTime = datetime.now()
                nSecond = 0
                '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''

            else:
                stage = "final"
                stagetwo = "inter"
                counter = counter + 1
                #HILO: Contabilizando la cantidad de repeticiones
                threading.Thread(target=text_correct_exercise, args=()).start()

                '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
                startCounter = True
                startTime = datetime.now()
                nSecond = 0
                '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''

        elif left_arm_hip_angle >= 85 and stagetwo=="inter":
            stage = "final"
            stagetwo = "final"
            feedback = "Subes mucho tu brazo"
            wrong_counter = wrong_counter + 1
            #Informando del error de flexion
            threading.Thread(target=text_to_speech, args=(feedback,)).start()

            '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
            startCounter = True
            startTime = datetime.now()
            nSecond = 0

    else:
        feedback = 'NO SE VE TU\n  CADERA O\n   BRAZO'
        #HILO: Creando el hilo que indica si se ven los puntos necesarios para el analisis
        threading.Thread(target=draw_cv2_error, args=(feedback, image,)).start()





#Ejercicio de flexion de hombro
def flexionHombro1(results, image):
    #Ingresando al global stage para modificarlo
    global stage, counter, wrong_counter

    #Verificando que se vean los puntos del brazo
    if (results.pose_landmarks.landmark[15].visibility > 0.90 and results.pose_landmarks.landmark[23].visibility > 0.90):

        left_arm_hip_angle = leftArmHipAngle(results, image,)
        left_arm_angle = leftArmAngle(results, image,)

        '''print('EL ANGULO ES: --------')
        print(left_arm_hip_angle)'''

        #HILO: Creando el draw bar
        threading.Thread(target=draw_cv2_bar, args=(left_arm_hip_angle,85,10,400, 150,image,)).start()

        if left_arm_hip_angle < 15:
            stage = "inicial"

        if left_arm_angle>140 and stage == "inicial":
            if left_arm_hip_angle > 75 and left_arm_hip_angle < 85 and stage == "inicial":


                    stage = "final"
                    counter = counter + 1

                    #HILO: Contabilizando la cantidad de repeticiones
                    threading.Thread(target=text_to_speech, args=(counter,)).start()

                #HILO: Abriendo el hilo que mide el tiempo entre los contadores


            elif left_arm_hip_angle > 85 and stage == "inicial":
                stage = "final"
                feedback = "Subes mucho el brazo"
                wrong_counter = wrong_counter + 1
                #Informando del error de flexion
                threading.Thread(target=text_to_speech, args=(feedback,)).start()
                '''threading.Thread(target=draw_cv2_error_flexion, args=(feedback, image,)).start()'''

            '''print('\nlos otros angulos\n')
            print(left_arm_angle)'''
        else:
            feedback = 'No dobles el brazo'
            # HILO: Informando del error de tiempo : muy rapido!!!
            threading.Thread(target=text_to_speech, args=(feedback,)).start()


    else:
        feedback = 'NO SE VE TU\n  CADERA O\n   BRAZO'
        #HILO: Creando el hilo que indica si se ven los puntos necesarios para el analisis
        threading.Thread(target=draw_cv2_error, args=(feedback, image,)).start()














'''---------------------------- FINALIZA: FEEDBACK DE LOS EJERCICIOS - FORTALECIMIENTO - TREN INFERIOR ---------------------------------------------------'''
















'''++++++++++++++++++++++++++++++++++++ OBTENIENDO EL PROCESAMIENTO DE POSES ++++++++++++++++++++++++++++++++++++++++++++++'''
#------------------------------- FLEXION CODO ------------------------------------------
def pose_estimation_flexion_codo(image, amount, serie, asignadoChoose):
    #Obteniendo las variables globales
    global counter, exercise_serie, mp_pose, mp_drawing, cumplimientoObjectUpdate, montoNecesario, cumplimientoflag
    cumplimientoObjectUpdate = asignadoChoose
    montoNecesario = amount
    #Variable resultados
    if counter<amount and exercise_serie<serie:
        # Extract landmarks
        try:
            # Obteniendo el result pose
            results = poseProcess(image)
            if results.pose_landmarks is not None:
                #Ingresando al target que hara el calculo de angulos corporales
                threading.Thread(target=flexionCodo, args=(results, image), kwargs={}).start()
                # dandole a cumplimiento el valor de counter
                cumplimientoflag = counter
        except:
            pass
        #HILO: Dibuja sobre el cv2 los contadores y numeros
        threading.Thread(target=draw_cv2, args=(image,)).start()
    elif exercise_serie<serie:
        '''EN CASO DE QUE EL EJERCICIO HAYA CUMPLIDO CON EL CONTADOR PERO AUN NO CON LA SERIE'''
        #HILO: Contador hacia atras para descanso
        threading.Thread(target=time_counter, args=(image,)).start()
    else:
        # HILO: Contador que salta un mensaje de finalizacion serie y
        #devuelve todos los valores a su valor original
        threading.Thread(target=serie_counter, args=(image,)).start()
    return image




# ----------------------------------- FLEXION DE HOMBRO HACIA ADELANTE ----------------------------
def pose_estimation_flexion_hombro_adelante(image, amount, serie, asignadoChoose):
    #Obteniendo las variables globales
    global counter, exercise_serie, mp_pose, mp_drawing, cumplimientoObjectUpdate, montoNecesario, cumplimientoflag
    cumplimientoObjectUpdate = asignadoChoose
    montoNecesario = amount
    #Variable resultados
    if counter<amount and exercise_serie<serie:
        # Extract landmarks
        try:
            # Obteniendo el result pose
            results = poseProcess(image)
            if results.pose_landmarks is not None:
                #Ingresando al target que hara el calculo de angulos corporales
                threading.Thread(target=flexionHombro, args=(results, image), kwargs={}).start()
                # dandole a cumplimiento el valor de counter
                cumplimientoflag = counter
        except:
            pass
        #HILO: Dibuja sobre el cv2 los contadores y numeros
        threading.Thread(target=draw_cv2, args=(image,)).start()
    elif exercise_serie<serie:
        '''EN CASO DE QUE EL EJERCICIO HAYA CUMPLIDO CON EL CONTADOR PERO AUN NO CON LA SERIE'''
        #HILO: Contador hacia atras para descanso
        threading.Thread(target=time_counter, args=(image,)).start()
    else:
        # HILO: Contador que salta un mensaje de finalizacion serie y
        #devuelve todos los valores a su valor original
        threading.Thread(target=serie_counter, args=(image,)).start()
    return image



# ----------------------------------- ABDUCCION HOMBRO LATERAL ----------------------------------
def pose_estimation_abduccion_hombro_lateral(image, amount, serie, asignadoChoose):
    #Obteniendo las variables globales
    global counter, exercise_serie, mp_pose, mp_drawing, cumplimientoObjectUpdate, montoNecesario
    cumplimientoObjectUpdate = asignadoChoose
    montoNecesario = amount
    #Variable resultados
    if counter<amount and exercise_serie<serie:
        # Extract landmarks
        try:
            #Obteniendo el result pose
            results = poseProcess(image)

            height, width, _ = image.shape


            '''if results.pose_landmarks is not None:
                #Ingresando al target que hara el calculo de angulos corporales
                threading.Thread(target=flexionHombro, args=(results, image), kwargs={}).start()'''


        except:
            pass

        #HILO: Dibuja sobre el cv2 los contadores y numeros
        threading.Thread(target=draw_cv2, args=(image,)).start()

        '''EN CASO DE QUE EL EJERCICIO HAYA CUMPLIDO CON EL CONTADOR PERO AUN NO CON LA SERIE'''
    elif exercise_serie<serie:
        #HILO: Contador hacia atras para descanso
        threading.Thread(target=time_counter, args=(image,)).start()
    else:
        # HILO: Contador que salta un mensaje de finalizacion serie y
        #devuelve todos los valores a su valor original
        threading.Thread(target=serie_counter, args=(image,)).start()


    return image

'''++++++++++++++++++++++++++++++++++++ FINALIZA: OBTENIENDO EL PROCESAMIENTO DE POSES ++++++++++++++++++++++++++++++++++++++++++++++'''







'''---------------------- CONTADOR DE TIEMPO - UNA VEZ TERMINADA LA SESION CONTARA 30 SEGUNDOS PARA LA SGTE --------------------------'''
def time_counter(image):
    global ml, se, counter, exercise_serie, cumplimientoflag, stage, stagetwo
    global cumplimientoObjectUpdate, wrong_counter, montoNecesario

    aciertos = round(((1 - (wrong_counter / montoNecesario)) * 100),2)

    #preguntando el flag
    if(cumplimientoflag>0):
        cumplimientoflag = 0
        # retornando los valores a su valor original
        print("wrong counter " + str(wrong_counter))
        print("monto necesario" + str(montoNecesario))
        cumplimientoObjectUpdate.update({'aciertos': aciertos })
        function.saveCumplimiento(cumplimientoObjectUpdate)

    #-------------Texto de cantidad de aciertos que se pondra
    aciertos_text = ''
    aciertos_color= (0,0,0)
    if aciertos<=60:
        aciertos_color = (0,0,255)
        aciertos_text = "Puedes hacerlo mejor!!!"
    elif aciertos>60 and aciertos<=75:
        aciertos_color = (0,255,255)
        aciertos_text = "Puedes mejorar!!!"
    elif aciertos>75:
        aciertos_color =(0,255,0)
        aciertos_text  = "Genial!!!"
    aciertos_porcentaje = f'Aciertos: {aciertos}%'


    #------------Comienza el contador de segundos
    if (se >= 0):
        ml = ml + 1
        '''Colocando un circulo en el centro que pinte el tiempo'''
        cv2.circle(image, (300,240), 150, (255,255,255), thickness=5, lineType=8, shift=0)
        cv2.putText(image, str(se),(260, 260),cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 6, cv2.LINE_AA)


        #Colocando un rectangulo que diga el porcentaje de error que tuvo
        cv2.rectangle(image, (130, 320), (470, 430), (102, 51, 0) , -1)
        cv2.putText(image, aciertos_porcentaje, (190, 360), cv2.FONT_HERSHEY_SIMPLEX, 0.8, aciertos_color, 2, cv2.LINE_AA)
        cv2.putText(image, aciertos_text, (160, 400), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        if ml == 50:
            ml = 0
            se = se - 1
            print(f'Tiempo segundos {se}')

    else:
        if(counter>0):
            #retornando los valores a su valor original
            counter = 0
            se = 5
            ml = 0
            #aumentando el valor de la serie
            exercise_serie = exercise_serie + 1
            wrong_counter = 0
            stage = ''
            stagetwo = ''

'''---------------------- FINALIZA - UNA VEZ TERMINADA LA SESION CONTARA 30 SEGUNDOS PARA LA SGTE --------------------------'''


'''---------------------- CONTADOR DE SERIE - UNA VEZ TERMINADA LA SERIE TERMINARA LA SESION --------------------------'''
def serie_counter(image):
    '''Retornando las variables a su valor original'''
    cv2.rectangle(image, (150, 170), (550, 340), (102, 51, 0), -1)
    '''Terminando la sesion'''
    cv2.putText(image, 'SE TERMINO LA SESION',(160, 240),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(image, ' PRESIONA "VOLVER" ', (160, 280), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    # Esto vera el estado si es down o up


'''---------------------- CONTADOR DE SERIE - UNA VEZ TERMINADA LA SERIE TERMINARA LA SESION  --------------------------'''
