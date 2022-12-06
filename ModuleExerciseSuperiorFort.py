import cv2
import numpy as np
import threading
import pyttsx3
import time
from kivymd.app import MDApp
import mediapipe as mp
from datetime import datetime

# the duration (in seconds)
duration = 5


'''++++++++++++++++++++++++++++ EL VALOR DEL TIME PRUEBA ++++++++++++++++++++++++++++++++++++'''
#El inicio del valor diff
diff = 0
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



'''++++++++++++++++++++++++++++ EL VALOR DEL TIME PRUEBA ++++++++++++++++++++++++++++++++++++'''

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
stage = ''

#Esto contara todas las repeticiones del ejercicio
counter = 0
#La series del ejercicio
exercise_serie = 0

#Esto contara las repeticiones erroneas
wrong_counter = 0

#El tiempo del ejercicio
time_exercise = 3.5

#Tiempo entre sesiones-----------
ml = 0
se = 5

dir = 0




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
    cv2.rectangle(image, (0, 0), (200, 50), (255, 0, 0), -1)
    cv2.rectangle(image, (202, 0), (265, 50), (255, 0, 0), 2)
    cv2.putText(image, "Contador:", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(image, "{}".format(counter), (220, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (128, 0, 250), 2)

    #Contador de erroneas
    cv2.rectangle(image, (0, 50), (200, 100), (255, 255, 0), -1)
    cv2.rectangle(image, (202, 50), (265, 100), (255, 255, 0), 2)
    cv2.putText(image, "Erroneas:", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(image, "{}".format(wrong_counter), (220, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (128, 0, 250), 2)




'''FUNCION QUE DIBUJA LOS LANDMARKS'''
def draw_landmark(results, mp_drawing, mp_pose, image ):
    # Render detections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

'''---------------------------- FINALIZA: DIBUJANDO LA IMAGEN QUE SALDRA ---------------------------------------------------'''




'''---------------------------- OBTENIENDO LA IMAGEN SOLO DE LOS PUNTOS ---------------------------------------------------'''

#Dibujando solo los puntos y lineas del brazo
def draw_left_arm(results, image):
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
    else:
        color_line = (0, 0, 255)
        color_circle = (0, 0, 255)

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
    else:
        color_line = (0, 0, 255)
        color_circle = (0, 0, 255)

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

    cv2.rectangle(image, (150, 180), (550, 340), (102, 51, 0), -1)

    y0, dy = 220, 50
    for i, line in enumerate(texto_error.split('\n')):
        y = y0 + i * dy
        cv2.putText(image, line, (200, y),fontFace, fontScale, (255, 255, 255), thickness, cv2.LINE_AA)







'''FUNCION QUE DIBUJA SOBRE EL CV2'''
draw_cv2_error_counter = 0
def draw_cv2_error_flexion(texto_error, image):
    global draw_cv2_error_counter
    print("ENTRE AL DRAW CV2_ ERROR")
    print(draw_cv2_error_counter)
    while(draw_cv2_error_counter>0):
        cv2.rectangle(image, (100, 200), (600, 400), (245, 117, 16), -1)
        # Rep data
        cv2.putText(image, texto_error, (120, 270),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3, cv2.LINE_AA)
        time.sleep(1)
        draw_cv2_error_counter = draw_cv2_error_counter - 1
        print('EL COUNTER')
        print(draw_cv2_error_counter)


'''FUNCION QUE DIBUJA SOBRE EL CV2'''
def draw_cv2_error_time(texto_error, image):
    duration = 10
    # HILO: Abriendo el hilo que mide el tiempo entre los contadores
    diff = 0
    while (diff <= duration):
        cv2.rectangle(image, (100, 200), (600, 400), (245, 117, 16), -1)
        # Rep data
        cv2.putText(image, texto_error, (120, 270),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3, cv2.LINE_AA)
        diff=diff+1
        time.sleep(0.5)





'''FUNCION QUE DIBUJA LOS LANDMARKS'''
def draw_landmark_2(results, mp_drawing, mp_pose, image ):
    # Render detections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))




'''---------------------------- FINALIZA: DIBUJANDO LOS ERRORES ---------------------------------------------------'''






'''---------------------------- DIBUJANDO EL BAR ---------------------------------------------------'''
'''FUNCION QUE DIBUJA SOBRE EL CV2'''
def draw_cv2_bar(angle, max, min, image):
    #Obteniendo los valores globales
    global count, dir, stage
    # Check for the dumbbell curls
    color = (255, 0, 255)
    if stage == 'inicial':
        color = (255,255,255)
        # angle = detector.findAngle(img, 11, 13, 15,False)
        '''per = np.interp(angle, (170, 90), (0, 100))
        bar = np.interp(angle, (170, 90), (650, 100))'''

        #valor del bar
        bar = np.interp(angle, (min, max), (400, 150))


        #print('ES EL BAR')
        #print(bar)
        # print(angle, per)

        # Draw Bar
        #Rectangulo general
        cv2.rectangle(image, (120, 150), (160, 400), color, 3)
        #Llenando el rectangulo
        cv2.rectangle(image, (120, int(bar)), (160, 400), color, cv2.FILLED)

    else:
        # Draw Bar
        cv2.rectangle(image, (120, 150), (160, 400), color, 3)



def draw_performance_bar(self, img, per, bar, color, count):
    cv2.rectangle(img, (1600, 100), (1675, 650), color, 3)
    cv2.rectangle(img, (1600, int(bar)), (1675, 650), color, cv2.FILLED)
    cv2.putText(
        img, f"{int(per)} %", (1600, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4
    )





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


def thread_timer(image):
    global startCounter, nSecond, totalSec, diff, startTime, timeElapsed, saveCount

    if startCounter:
        if nSecond < totalSec:
            # draw the Nth second on each frame
            cv2.putText(image, strSec[nSecond], (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 255, 255), 2,cv2.LINE_AA)  # adding timer text

            time.sleep(1)
            timeElapsed = (datetime.now() - startTime).total_seconds()
            #            print 'timeElapsed: {}'.format(timeElapsed)

            if timeElapsed >= 1:
                nSecond += 1
                #                print 'nthSec:{}'.format(nSecond)
                timeElapsed = 0
                startTime = datetime.now()
            print("TIME ELAPSED " + str(nSecond))

        else:
            saveCount += 1
            startCounter = False
            nSecond = 1



def thread_timer_prueba1(image, duration):
    global diff
    #Esto obtiene la hora actual
    start_time = datetime.now()
    #Esto obtiene un segundo
    time.sleep(60)
    '''print("Start : %s" % time.ctime())
    time.sleep(5)
    print("End : %s" % time.ctime())'''
    sumatiempo = (datetime.now() - start_time).seconds  # converting into seconds
    print(" HOLA ESTE ES EL DIFF "+str(diff))
    if (diff <= duration):
        cv2.putText(image, str(diff), (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2,
                    cv2.LINE_AA)  # adding timer text
        cv2.imshow('frame', image)
        diff = diff + sumatiempo



def thread_timer_mantener_extra():
    global time_exercise
    # EL LOOP
    start_time1 = time.process_time()
    time.sleep(2)
    end_time1 = time.process_time()
    time_exercise = end_time1 - start_time1

    print("The time spent in thread is {}".format(end_time1 - start_time1))
'''-------------------------- FINALIZA: ESTOS SON LOS EXTRAS  -----------------------------------------'''




'''---------------------------- FEEDBACK DE LOS EJERCICIOS - FORTALECIMIENTO - TREN INFERIOR ---------------------------------------------------'''

#Ejercicio de flexion de codo
def flexionCodo(results, image):
    #Ingresando al global stage para modificarlo
    global stage, counter, time_exercise, wrong_counter, draw_cv2_error_counter

    #Verificando que se vean los puntos del brazo
    if (results.pose_landmarks.landmark[13].visibility > 0.90 and results.pose_landmarks.landmark[15].visibility > 0.90):
        left_arm_angle = leftArmAngle(results, image,)
        '''print('EL ANGULO ES: --------')
        print(left_arm_angle)'''
        #HILO: Creando el draw bar

        threading.Thread(target=draw_cv2_bar, args=(left_arm_angle,160,90,image,)).start()

        '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
        global startCounter, nSecond, totalSec, diff, timeElapsed, saveCount
        global startTime, keyPressTime
        if stage == "inicial":
            if startCounter:
                if nSecond < totalSec:
                    # draw the Nth second on each frame
                    cv2.putText(image, strSec[nSecond], (300, 300), cv2.FONT_HERSHEY_SIMPLEX, 6, (255, 255, 255), 2,
                                cv2.LINE_AA)  # adding timer text

                    #time.sleep(1)
                    timeElapsed = (datetime.now() - startTime).total_seconds()
                    #            print 'timeElapsed: {}'.format(timeElapsed)

                    if timeElapsed >= 1:
                        nSecond += 1
                        #                print 'nthSec:{}'.format(nSecond)
                        timeElapsed = 0
                        startTime = datetime.now()
                    print("TIME ELAPSED " + str(nSecond))

                else:
                    saveCount += 1
                    startCounter = False
                    nSecond = 1
            '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''


            '''threading.Thread(target=thread_timer, args=(image,)).start()'''



        if left_arm_angle > 160:
            stage = "inicial"

        if left_arm_angle > 80 and left_arm_angle < 90 and stage == "inicial":
            if time_exercise<2.0:
                stage = 'final'
                time_exercise = 0.0
                wrong_counter = wrong_counter + 1
                feedback = 'muy rapido'
                #HILO: Informando del error de tiempo : muy rapido!!!
                #threading.Thread(target=text_to_speech, args=(feedback,)).start()
                threading.Thread(target=draw_cv2_error_time, args=(feedback, image,)).start()

            else:
                stage = "final"
                counter = counter + 1
                print(time_exercise)
                #HILO: Contabilizando la cantidad de repeticiones
                threading.Thread(target=text_to_speech, args=(counter,)).start()
                # HILO: Abriendo el hilo que mide el tiempo entre los contadores
                '''threading.Thread(target=thread_timer, args=()).start()'''

                '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''
                startCounter = True
                startTime = datetime.now()
                '''xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'''




        elif left_arm_angle < 70 and stage == "inicial":
            draw_cv2_error_counter = 20
            stage = "final"
            feedback = "Flexionas mucho tu brazo"
            wrong_counter = wrong_counter + 1

            # HILO: Abriendo el hilo que mide el tiempo entre los contadores
            '''threading.Thread(target=thread_timer, args=()).start()'''
            #Informando del error de flexion
            threading.Thread(target=text_to_speech, args=(feedback,)).start()
            '''threading.Thread(target=draw_cv2_error_flexion, args=(feedback, image,)).start()'''

        '''print('\nlos otros angulos\n')
        print(left_arm_angle)'''

    else:
        feedback = '  NO SE VE\n  TU BRAZO'
        #HILO: Creando el hilo que indica si se ven los puntos necesarios para el analisis
        threading.Thread(target=draw_cv2_error, args=(feedback, image,)).start()





#Ejercicio de flexion de hombro
def flexionHombro(results, image):
    #Ingresando al global stage para modificarlo
    global stage, counter, time_exercise, wrong_counter

    #Verificando que se vean los puntos del brazo
    if (results.pose_landmarks.landmark[15].visibility > 0.90 and results.pose_landmarks.landmark[23].visibility > 0.90):

        left_arm_hip_angle = leftArmHipAngle(results, image,)
        left_arm_angle = leftArmAngle(results, image,)

        '''print('EL ANGULO ES: --------')
        print(left_arm_hip_angle)'''

        #HILO: Creando el draw bar
        threading.Thread(target=draw_cv2_bar, args=(left_arm_hip_angle,85,10,image,)).start()

        if left_arm_hip_angle < 15:
            stage = "inicial"

        if left_arm_angle>140 and stage == "inicial":
            if left_arm_hip_angle > 75 and left_arm_hip_angle < 85 and stage == "inicial":

                if time_exercise<1.8:
                    stage = 'final'
                    time_exercise = 0.0
                    wrong_counter = wrong_counter + 1
                    feedback = 'Hazlo mas lento!!!'
                    #HILO: Informando del error de tiempo : muy rapido!!!
                    threading.Thread(target=draw_cv2_error_time, args=(feedback, image,)).start()

                else:
                    stage = "final"
                    counter = counter + 1
                    print(time_exercise)
                    #HILO: Contabilizando la cantidad de repeticiones
                    threading.Thread(target=text_to_speech, args=(counter,)).start()

                #HILO: Abriendo el hilo que mide el tiempo entre los contadores
                threading.Thread(target=thread_timer, args=()).start()


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
def pose_estimation_flexion_codo(image, amount, serie):
    #Obteniendo las variables globales
    global counter, exercise_serie, mp_pose, mp_drawing
    #Variable resultados
    if counter<=amount and exercise_serie<=serie:
        # Extract landmarks
        try:
            # Obteniendo el result pose
            results = poseProcess(image)
            if results.pose_landmarks is not None:
                #Ingresando al target que hara el calculo de angulos corporales
                threading.Thread(target=flexionCodo, args=(results, image), kwargs={}).start()
        except:
            pass

        #HILO: Dibuja sobre el cv2 los contadores y numeros
        threading.Thread(target=draw_cv2, args=(image,)).start()

        # HILO: Dibuja los puntos del cuerpo
        '''threading.Thread(target=draw_landmark, args=(results, mp_drawing, mp_pose, image,)).start()'''

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
def pose_estimation_flexion_hombro_adelante(image, amount, serie):
    #Obteniendo las variables globales
    global counter, exercise_serie, mp_pose, mp_drawing
    #Variable resultados
    if counter<=amount and exercise_serie<=serie:
        # Extract landmarks
        try:
            #Obteniendo el result pose
            results = poseProcess(image)
            if results.pose_landmarks is not None:
                #Ingresando al target que hara el calculo de angulos corporales
                threading.Thread(target=flexionHombro, args=(results, image), kwargs={}).start()


        except:
            pass

        #HILO: Dibuja sobre el cv2 los contadores y numeros
        threading.Thread(target=draw_cv2, args=(image,)).start()

        # HILO: Dibuja los puntos del cuerpo
        '''threading.Thread(target=draw_landmark, args=(results, mp_drawing, mp_pose, image,)).start()'''


        '''EN CASO DE QUE EL EJERCICIO HAYA CUMPLIDO CON EL CONTADOR PERO AUN NO CON LA SERIE'''
    elif exercise_serie<serie:
        #HILO: Contador hacia atras para descanso
        threading.Thread(target=time_counter, args=(image,)).start()
    else:
        # HILO: Contador que salta un mensaje de finalizacion serie y
        #devuelve todos los valores a su valor original
        threading.Thread(target=serie_counter, args=(image,)).start()


    return image




# ----------------------------------- ABDUCCION HOMBRO LATERAL ----------------------------------
def pose_estimation_abduccion_hombro_lateral(image, amount, serie):
    #Obteniendo las variables globales
    global counter, exercise_serie, mp_pose, mp_drawing
    #Variable resultados
    if counter<=amount and exercise_serie<=serie:
        # Extract landmarks
        try:
            #Obteniendo el result pose
            results = poseProcess(image)

            height, width, _ = image.shape
            print('HOMBRO IZQUIERDO')
            print(int(results.pose_landmarks.landmark[11].y * height))
            print('HOMBRO DERECHO')
            print(int(results.pose_landmarks.landmark[12].y * height))


            '''if results.pose_landmarks is not None:
                #Ingresando al target que hara el calculo de angulos corporales
                threading.Thread(target=flexionHombro, args=(results, image), kwargs={}).start()'''


        except:
            pass

        #HILO: Dibuja sobre el cv2 los contadores y numeros
        threading.Thread(target=draw_cv2, args=(image,)).start()

        # HILO: Dibuja los puntos del cuerpo
        '''threading.Thread(target=draw_landmark, args=(results, mp_drawing, mp_pose, image,)).start()'''


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
    global ml, se, counter, exercise_serie
    if (se >= 0):
        ml = ml + 1
        '''Colocando un circulo en el centro que pinte el tiempo'''
        cv2.circle(image, (300,240), 150, (255,255,255), thickness=5, lineType=8, shift=0)
        cv2.putText(image, str(se),(260, 260),cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 6, cv2.LINE_AA)
        if ml == 60:
            ml = 0
            se = se - 1
            print(f'Tiempo segundos {se}')
    else:
        counter = 0
        se = 10
        ml = 0
        exercise_serie = exercise_serie + 1


'''---------------------- FINALIZA - UNA VEZ TERMINADA LA SESION CONTARA 30 SEGUNDOS PARA LA SGTE --------------------------'''


'''---------------------- CONTADOR DE SERIE - UNA VEZ TERMINADA LA SERIE TERMINARA LA SESION --------------------------'''
def serie_counter(image):
    '''Retornando las variables a su valor original'''
    global stage, counter, exercise_serie, wrong_counter, time_exercise, ml, se, dir
    '''Terminando la sesion'''
    cv2.putText(image, 'SE TERMINO LA SESION',(260, 260),cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 6, cv2.LINE_AA)
    # Esto vera el estado si es down o up
    stage = ''

    # Esto contara todas las repeticiones del ejercicio
    counter = 0
    # La series del ejercicio
    exercise_serie = 0

    # Esto contara las repeticiones erroneas
    wrong_counter = 0

    # El tiempo del ejercicio
    time_exercise = 3.5

    # Tiempo entre sesiones-----------
    ml = 0
    se = 5

    dir = 0
    MDApp.get_running_app().root.current = 'menu'



'''---------------------- CONTADOR DE SERIE - UNA VEZ TERMINADA LA SERIE TERMINARA LA SESION  --------------------------'''
