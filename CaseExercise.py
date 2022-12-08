
import ModuleExerciseSuperiorFort as moduleExerciseSuperiorFort
import ModuleExerciseSuperiorElong as moduleExerciseSuperiorElong
import ModuleExerciseInferiorFort as moduleExerciseInferiorFort
import ModuleExerciseInferiorElong as moduleExerciseInferiorElong



'''------------------- EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE INFERIOR-----------------------'''
def switch_inferior_fortalecimiento(image, ejercicio, amount, serie, asignadoChoose):
    #en caso de que sea igual a sentadilla entonces que lo lleve a ese
    if ejercicio == "Sentadilla":
        return moduleExerciseInferiorFort.pose_estimation_sentadilla(image, amount, serie, asignadoChoose)


def switch_inferior_elongacion(image, ejercicio, amount, serie, asignadoChoose):
    #en caso de que sea igual a sentadilla entonces que lo lleve a ese
    if ejercicio == "Flexion co":
        return moduleExerciseInferiorElong.pose_estimation_flexion_codo(image, amount, serie, asignadoChoose)

'''------------------- FINALIZA: EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE INFERIOR-----------------------'''



'''------------------- EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE SUPERIOR -----------------------'''
def switch_superior_fortalecimiento(image, ejercicio, amount, serie, asignadoChoose, data_map):
    #en caso de que sea igual a sentadilla entonces que lo lleve a ese
    if ejercicio == "Flexion codo":
        return moduleExerciseSuperiorFort.pose_estimation_flexion_codo(image, amount, serie, asignadoChoose, data_map)

    elif ejercicio == "Flexion hombro":
        return moduleExerciseSuperiorFort.pose_estimation_flexion_hombro_adelante(image, amount, serie, asignadoChoose, data_map)

    elif ejercicio == "Abduccion lateral":
        return moduleExerciseSuperiorFort.pose_estimation_abduccion_hombro_lateral(image, amount, serie, asignadoChoose, data_map)



def switch_superior_elongacion(image, ejercicio, amount, serie, asignadoChoose):
    #en caso de que sea igual a sentadilla entonces que lo lleve a ese
    if ejercicio == "Flexion co":
        return moduleExerciseSuperiorElong.pose_estimation_flexion_codo(image, amount, serie, asignadoChoose)

'''------------------- FINALIZA: EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE SUPERIOR -----------------------'''