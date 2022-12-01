import ModuleExercise as moduleExercise

'''------------------- EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE INFERIOR-----------------------'''
def switch_inferior_fortalecimiento(image, ejercicio, amount, serie):
    #en caso de que sea igual a sentadilla entonces que lo lleve a ese
    if ejercicio == "Flexion codo":
        return moduleExercise.pose_estimation_flexion_codo(image, amount, serie)

def switch_inferior_elongacion(image, ejercicio, amount, serie):
    #en caso de que sea igual a sentadilla entonces que lo lleve a ese
    if ejercicio == "Flexion codo":
        return moduleExercise.pose_estimation_flexion_codo(image, amount, serie)

'''------------------- FINALIZA: EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE INFERIOR-----------------------'''



'''------------------- EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE SUPERIOR -----------------------'''
def switch_superior_fortalecimiento(image, ejercicio, amount, serie):
    #en caso de que sea igual a sentadilla entonces que lo lleve a ese
    if ejercicio == "Flexion codo":
        return moduleExercise.pose_estimation_flexion_codo(image, amount, serie)


def switch_superior_elongacion(image, ejercicio, amount, serie):
    #en caso de que sea igual a sentadilla entonces que lo lleve a ese
    if ejercicio == "Flexion codo":
        return moduleExercise.pose_estimation_flexion_codo(image, amount, serie)

    elif ejercicio == "PHP":
        return "You can become a backend developer."

'''------------------- FINALIZA: EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE SUPERIOR -----------------------'''