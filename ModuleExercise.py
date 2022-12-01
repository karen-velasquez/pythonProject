import cv2
import math
import os
import numpy as np
import threading
import pyttsx3
import time
from kivymd.app import MDApp

from mediapipe.framework.formats import landmark_pb2
import mediapipe as mp

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









'''---------------------------- DIBUJANDO LA IMAGEN QUE SALDRA ---------------------------------------------------'''
'''FUNCION QUE DIBUJA SOBRE EL CV2'''
def draw_cv2(image):
    global counter, stage, wrong_counter
    #Estado de la posicion
    '''cv2.putText(image, 'STAGE', (65, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, stage,
                    (60, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
'''
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







'''---------------------------- FINALIZA: OBTENIENDO LA IMAGEN SOLO DE LOS PUNTOS ---------------------------------------------------'''











'''---------------------------- DIBUJANDO LOS ERRORES ---------------------------------------------------'''
'''FUNCION QUE DIBUJA SOBRE EL CV2'''
def draw_cv2_error(texto_error, image):
    cv2.rectangle(image, (100, 200), (600, 400), (245, 117, 16), -1)
                # Rep data
    cv2.putText(image, texto_error, (120, 270),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3, cv2.LINE_AA)


'''FUNCION QUE DIBUJA SOBRE EL CV2'''
def draw_cv2_error_flexion(texto_error, image):
    timer_error = 0
    cv2.rectangle(image, (100, 200), (600, 400), (245, 117, 16), -1)
                    # Rep data
    cv2.putText(image, texto_error, (120, 270),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3, cv2.LINE_AA)
    timer_error = timer_error + 1


'''FUNCION QUE DIBUJA SOBRE EL CV2'''
def draw_cv2_error_time(texto_error, image):
    cv2.rectangle(image, (100, 200), (600, 400), (245, 117, 16), -1)
                # Rep data
    cv2.putText(image, texto_error, (120, 270),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.4, (255, 255, 255), 3, cv2.LINE_AA)
    time.sleep(3)




'''FUNCION QUE DIBUJA LOS LANDMARKS'''
def draw_landmark_2(results, mp_drawing, mp_pose, image ):
    # Render detections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))




'''---------------------------- FINALIZA: DIBUJANDO LOS ERRORES ---------------------------------------------------'''






'''---------------------------- DIBUJANDO EL BAR ---------------------------------------------------'''
'''FUNCION QUE DIBUJA SOBRE EL CV2'''
def draw_cv2_bar(angle, image):
    #Obteniendo los valores globales
    global count, dir, stage

    # Check for the dumbbell curls
    color = (255, 0, 255)
    if stage == 'inicial':
        color = (255,255,255)
        # angle = detector.findAngle(img, 11, 13, 15,False)
        '''per = np.interp(angle, (170, 90), (0, 100))
        bar = np.interp(angle, (170, 90), (650, 100))'''
        #porcentaje
        per = np.interp(angle, (90, 160), (0, 150))
        #valor del bar
        bar = np.interp(angle, (90, 160), (400, 150))

        print('ES EL PER')
        print(per)

        print('ES EL BAR')
        print(bar)
        # print(angle, per)


        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0

        # Draw Bar
        #Rectangulo general
        cv2.rectangle(image, (120, 150), (160, 400), color, 3)

        #Llenando el rectangulo
        cv2.rectangle(image, (120, int(bar)), (160, 400), color, cv2.FILLED)
        cv2.putText(image, f'{int(per)} %', (120, 0), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)
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


'''---------------------------- FINALIZA: CALCULANDO LOS ANGULOS NECESARIOS ---------------------------------------------------'''




def thread_timer():
    global time_exercise
    # EL LOOP
    start_time1 = time.process_time()
    time.sleep(2)
    end_time1 = time.process_time()
    time_exercise = end_time1 - start_time1

    print("The time spent in thread is {}".format(end_time1 - start_time1))





'''---------------------------- FEEDBACK DE LOS EJERCICIOS - FORTALECIMIENTO - TREN INFERIOR ---------------------------------------------------'''
#Convirtiendo el texto en voz
def text_to_speech(feedback):
    engine.say(feedback)
    engine.runAndWait()



#Ejercicio de la sentadilla
def leftArm(results, image):
    #Ingresando al global stage para modificarlo
    global stage, counter, time_exercise, wrong_counter

    #Verificando que se vean los puntos del brazo
    if (results.pose_landmarks.landmark[13].visibility > 0.90 and results.pose_landmarks.landmark[15].visibility > 0.90):
        left_arm_angle = leftArmAngle(results, image,)
        print('EL ANGULO ES: --------')
        print(left_arm_angle)

        #HILO: Creando el draw bar

        threading.Thread(target=draw_cv2_bar, args=(left_arm_angle,image,)).start()

        if left_arm_angle > 160:
            stage = "inicial"

        if left_arm_angle > 80 and left_arm_angle < 90 and stage == "inicial":

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


        elif left_arm_angle < 70 and stage == "inicial":
            stage = "final"
            feedback = "Estas flexionando mucho tu brazo"
            wrong_counter = wrong_counter + 1
            #Informando del error de flexion
            threading.Thread(target=draw_cv2_error_flexion, args=(feedback, image,)).start()

        '''print('\nlos otros angulos\n')
        print(left_arm_angle)'''

    else:
        feedback = 'NO SE VE TU BRAZO'
        #HILO: Creando el hilo que indica si se ven los puntos necesarios para el analisis
        threading.Thread(target=draw_cv2_error, args=(feedback, image,)).start()



'''---------------------------- FINALIZA: FEEDBACK DE LOS EJERCICIOS - FORTALECIMIENTO - TREN INFERIOR ---------------------------------------------------'''


























'''++++++++++++++++++++++++++++++++++++ OBTENIENDO EL PROCESAMIENTO DE POSES ++++++++++++++++++++++++++++++++++++++++++++++'''
def pose_estimation_flexion_codo(image, amount, serie):
    #Obteniendo las variables globales
    global counter, exercise_serie, mp_pose, mp_drawing
    #Variable resultados
    results = ''
    if counter<=amount and exercise_serie<=serie:
        # Extract landmarks
        try:
            #Obteniendo el result pose
            results = poseProcess(image)
            landmarks = results.pose_landmarks.landmark

            #Ingresando al target que hara el calculo de angulos corporales
            threading.Thread(target=leftArm, args=(results, image), kwargs={}).start()


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
