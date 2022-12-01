import cv2
import math
import os
import numpy as np
import threading
import pyttsx3
import time
from kivymd.app import MDApp

from mediapipe.framework.formats import landmark_pb2


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

'''---------------------------- CONFIGURANDO LA VOZ---------------------------------------------------'''
engine2 = pyttsx3.init()
voices2 = engine2.getProperty('voices')
# verificando que la voz exista ****REVISAR LUEGO*****
number2 = 2
if (len(voices2) == number2):
    number2 = 0
    print('es mayor')
engine2.setProperty('voice', voices2[number2].id)
# controlando el rate, a higuer rate = mas rapido
engine2.setProperty('rate', 150)
'''---------------------------- FINALIZA: CONFIGURANDO LA VOZ---------------------------------------------------'''

'''---------------------------- CONFIGURANDO LA VOZ---------------------------------------------------'''
engine3 = pyttsx3.init()
voices3 = engine3.getProperty('voices')
# verificando que la voz exista ****REVISAR LUEGO*****
number3 = 2
if (len(voices3) == number3):
    number3 = 0
    print('es mayor')
engine3.setProperty('voice', voices3[number3].id)
# controlando el rate, a higuer rate = mas rapido
engine3.setProperty('rate', 150)
'''---------------------------- FINALIZA: CONFIGURANDO LA VOZ---------------------------------------------------'''










'''---------------------------- DIBUJANDO LA IMAGEN QUE SALDRA ---------------------------------------------------'''
'''FUNCION QUE DIBUJA SOBRE EL CV2'''
def draw_cv2(image):
    global counter, stage, wrong_counter
    cv2.rectangle(image, (0, 0), (300, 73), (245, 117, 16), -1)
    '''Realizando el conteo de repeticiones'''
    cv2.putText(image, 'REPS', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, str(counter),
                            (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
    '''Realizando la actualizacion de estado'''
    cv2.putText(image, 'STAGE', (65, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(image, stage,
                    (60, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
    '''Realizando el conteo de repeticiones erroneas'''
    cv2.putText(image, 'ERRONEAS', (150, 12),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    cv2.putText(image, str(wrong_counter),
                (150, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)


'''FUNCION QUE DIBUJA LOS LANDMARKS'''
def draw_landmark(results, mp_drawing, mp_pose, image ):

    # Render detections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

'''---------------------------- FINALIZA: DIBUJANDO LA IMAGEN QUE SALDRA ---------------------------------------------------'''


'''---------------------------- OBTENIENDO LA IMAGEN SOLO DE LOS PUNTOS ---------------------------------------------------'''

def draw_left_arm(results,  mp_drawing, image):
    #Confirgurando el color de la linea
    color_line = (255, 255, 255)
    color_circle = (0, 0, 255)

    landmark_subset = landmark_pb2.NormalizedLandmarkList(
        landmark=[
            results.pose_landmarks.landmark[13],
            results.pose_landmarks.landmark[14],
            results.pose_landmarks.landmark[25],
            results.pose_landmarks.landmark[26],
        ]
    )
    annotated_image = image.copy()
    mp_drawing.draw_landmarks(
        image=annotated_image,
        landmark_list=landmark_subset)

    '''x1 = np.array(a)[0]
    y1 = np.array(a)[1]  # First
    x2 = np.array(b)[0]
    y2 = np.array(b)[1]  # Second
    x3 = np.array(c)[0]
    y3 = np.array(c)[1]  # Third'''


#    cv2.line(image, (x1, y1), (x2, y2), color_line, 3)
 #   cv2.line(image, (x3, y3), (x2, y2), color_line, 3)
    '''cv2.circle(image, (x1, y1), 10, color_circle, cv2.FILLED)
    cv2.circle(image, (x1, y1), 15, color_circle, 2)
    cv2.circle(image, (x2, y2), 10, color_circle, cv2.FILLED)
    cv2.circle(image, (x2, y2), 15, color_circle, 2)
    cv2.circle(image, (x3, y3), 10, color_circle, cv2.FILLED)
    cv2.circle(image, (x3, y3), 15, color_circle, 2)'''
    '''cv2.putText(image, str(int(angle)), (x2 - 50, y2 + 50),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)'''

def findlist(results, image, draw=True):
    lmList = []
    if results.pose_landmarks:
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = image.shape
            # print(id, lm)
            cx, cy = int(lm.x * w), int(lm.y * h)
            lmList.append([id, cx, cy])
            if draw:
                cv2.circle(image, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
    return lmList



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
    time.sleep(2)



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
    global count, dir
    # angle = detector.findAngle(img, 11, 13, 15,False)
    '''per = np.interp(angle, (170, 90), (0, 100))
    bar = np.interp(angle, (170, 90), (650, 100))'''

    per = np.interp(angle, (90, 160), (0, 20))
    bar = np.interp(angle, (90, 160), (400, 60))

    print('ES EL PER')
    print(per)

    print('ES EL BAR')
    print(bar)
    # print(angle, per)

    # Check for the dumbbell curls
    color = (255, 0, 255)
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
    cv2.rectangle(image, (120, 40), (175, 60), color, 3)
    cv2.rectangle(image, (120, int(bar)), (175, 60), color, cv2.FILLED)
    cv2.putText(image, f'{int(per)} %', (120, 0), cv2.FONT_HERSHEY_PLAIN, 4,
                color, 4)


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
def leftArmAngle(landmarks, mp_pose, image):
    '''Obteniendo los puntos------'''
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


    if (landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].visibility > 0.90 and landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility > 0.90):
        threading.Thread(target=draw_left_arm, args=(landmarks, mp_pose, image,)).start()

        return calculate_angle(left_shoulder, left_elbow, left_wrist)


    else:
        return 0

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

#Convirtiendo el texto en voz
def text_to_speech2(feedback):
    engine2.say(feedback)
    engine2.runAndWait()

#Convirtiendo el texto en voz
def text_to_speech3(feedback):
    engine3.say(feedback)
    engine3.runAndWait()


#Ejercicio de la sentadilla
def sentadilla(landmarks, mp_pose, image):
    #Ingresando al global stage para modificarlo
    global stage, counter, time_exercise


    #creando la lista de hilos
    list_threads = []

    #Obteniendo el angulo
    left_arm_angle = leftArmAngle(landmarks, mp_pose, image,)
    print('EL ANGULO ES: --------')
    print(left_arm_angle)

    if left_arm_angle != 0:

        '''----CREANDO UN HILO QUE EL CV2 BAR---'''
        target_thread_draw = threading.Thread(target=draw_cv2_bar, args=(left_arm_angle,image,))
        target_thread_draw.start()



        if left_arm_angle > 160:
            stage = "inicial"
        if left_arm_angle > 80 and left_arm_angle < 90 and stage == "inicial":

            if time_exercise<1.8:
                time_exercise = 0.0
                feedback = 'Hazlo mas lento!!!'
                print('EL NUMERO ES:\n')
                print('--------------------------------')
                threading.Thread(target=draw_cv2_error_time, args=(feedback, image,)).start()
                #threading.Thread(target=text_to_speech2, args=(feedback,)).start()
            else:

                counter = counter + 1
                print('EL NUMERO ES:\n')
                print(counter)
                stage = "final"
                print(time_exercise)
                threading.Thread(target=text_to_speech2, args=(counter,)).start()
            #Abriendo el hilo que mide el tiempo entre los contadores
            threading.Thread(target=thread_timer, args=()).start()



        elif left_arm_angle < 70 and stage == "inicial":
            global wrong_counter

            feedback = "Estas flexionando mucho tu brazo"
            wrong_counter = wrong_counter + 1
            stage = "final"


            # Abriendo el hilo que dara la retroalimentacion
            '''print('el angulo de error\n')'''

            target_thread_draw = threading.Thread(
                target=draw_cv2_error_flexion, args=(feedback, image,)
            )
            list_threads.append(target_thread_draw)
            target_thread_draw.start()

        '''print('\nlos otros angulos\n')
        print(left_arm_angle)'''

    else:
        feedback = 'NO SE VE TU BRAZO'
        '''----CREANDO UN HILO QUE EL CV2---'''
        target_thread_draw = threading.Thread(
            target=draw_cv2_error, args=(feedback, image,)
        )
        list_threads.append(target_thread_draw)
        target_thread_draw.start()


        #threading.Thread(target=text_to_speech3, args=(feedback,)).start()
        '''speaker_thread_3 = threading.Thread(
            target=text_to_speech3, args=(feedback,), kwargs={}
        )
        list_threads.append(speaker_thread_3)
        speaker_thread_3.start()
'''


'''---------------------------- FINALIZA: FEEDBACK DE LOS EJERCICIOS - FORTALECIMIENTO - TREN INFERIOR ---------------------------------------------------'''


























'''---------------------------------- OBTENIENDO EL PROCESAMIENTO DE POSES-----------------------------------------------------------'''




def pose_estimation_sentadilla(image, mp_drawing, mp_pose, results, amount, serie):
    global counter, exercise_serie
    if counter<=amount and exercise_serie<=serie:
        list_threads = []
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            #left_leg_angle(landmarks, mp_pose)
            '''----CREANDO UN CALCULE LOS ANGULOS CORPORALES----'''
            target_thread_draw = threading.Thread(
                target=sentadilla, args=(landmarks, mp_pose, image), kwargs={}
            )
            list_threads.append(target_thread_draw)
            target_thread_draw.start()

            '''angle = sentadilla(landmarks, mp_pose)
            print(angle)
    
                # Visualize angle
            cv2.putText(image, str('hklj'),
                        (100, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                        )'''
        except:
            pass




        '''----CREANDO UN HILO QUE EL CV2---'''
        target_thread_draw = threading.Thread(
                target=draw_cv2, args=(image,)
            )
        list_threads.append(target_thread_draw)
        target_thread_draw.start()

        '''----CREANDO UN HILO QUE DIBUJE LOS PUNTOS----'''
        '''target_thread_landmark = threading.Thread(
            target=draw_landmark, args=(results, mp_drawing, mp_pose, image, )
        )
        list_threads.append(target_thread_landmark)
        target_thread_landmark.start()'''




    #REVISAR PORQUE SE PARA RECIEN EN LA TERCERA
    elif exercise_serie<serie:
        '''----CREANDO QUE CREE LOS PUNTOS----'''
        #threading.Thread(target=time_counter, args=(image,)).start()
        threading.Thread(target=time_counter, args=(image,)).start()
    else:
        threading.Thread(target=serie_counter, args=(image,)).start()


    return image





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
