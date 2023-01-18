import ModuleExerciseSuperiorFort as moduleExerciseSuperiorFort
import ModuleExerciseInferiorFort as moduleExerciseInferiorFort
import TwoModuleExerciseSuperiorFort as twoModuleExerciseSuperiorFort

def returnValues():
    moduleExerciseSuperiorFort.returnValuesOriginal()


'''------------------- EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE INFERIOR-----------------------'''
def switch_inferior_fortalecimiento(image, ejercicio, amount, serie, asignadoChoose):
    #en caso de que sea igual a sentadilla entonces que lo lleve a ese
    if ejercicio == "Estocada":
        return moduleExerciseInferiorFort.pose_estimation_estocada(image, amount, serie, asignadoChoose)
    elif ejercicio == "Sentadilla":
        return moduleExerciseInferiorFort.pose_estimation_sentadilla(image, amount, serie, asignadoChoose)

'''------------------- FINALIZA: EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE INFERIOR-----------------------'''









'''------------------- EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE SUPERIOR -----------------------'''
def switch_superior_fortalecimiento(image, ejercicio, amount, serie, asignadoChoose):
    #en caso de que sea igual a sentadilla entonces que lo lleve a ese
    if ejercicio == "Flexion codo":
        return moduleExerciseSuperiorFort.pose_estimation_flexion_codo(image, amount, serie, asignadoChoose)

    elif ejercicio == "Flexion hombro":
        return moduleExerciseSuperiorFort.pose_estimation_flexion_hombro_adelante(image, amount, serie, asignadoChoose)

    elif ejercicio == "Abduccion lateral":
        return moduleExerciseSuperiorFort.pose_estimation_abduccion_hombro_lateral(image, amount, serie, asignadoChoose)

    elif ejercicio == "Remos dorsales":
        return twoModuleExerciseSuperiorFort.pose_estimation_remos_dorsales(image, amount, serie, asignadoChoose)


'''------------------- FINALIZA: EN CASO DE QUE EL EJERCICIO SEA DE LA PARTE SUPERIOR -----------------------'''