
import cv2
import ModuleExercise as moduleExercise

#funcion que enviara los datos a procesar
def poseProcess(frame, pose, mp_drawing, mp_pose, ejercicio, amount, serie):
    # Recolor image to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False

    # Make detection
    results = pose.process(image)

    # Recolor back to BGR
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return switch(image, mp_drawing, mp_pose, results, ejercicio, amount, serie)




def switch(image, mp_drawing, mp_pose, results, ejercicio, amount, serie):
    #en caso de que sea igual a sentadilla entonces que lo lleve a ese
    if ejercicio == "Flexion codo":
        return moduleExercise.pose_estimation_sentadilla(image, mp_drawing, mp_pose, results, amount, serie)

    elif ejercicio == "PHP":
        return "You can become a backend developer."