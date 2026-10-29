from collections import namedtuple
from math import sqrt

EstacionSevici = namedtuple("EstacionSevici", 
    "nombre, direccion, latitud, longitud, capacidad, puestos_libres, bicicletas_disponibles")

def selecciona_color(estacion:EstacionSevici) -> str:
    """
    Devuelve el color en que debe pintarse cada estación según su disponibilidad.

    Parámetros:
    estacion: EstacionSevici

    Devuelve:
    str: "green", "orange", "red" o "gray"
    """
    if estacion.capacidad == 0:
        return "gray"
    disp = int(estacion.bicicletas_disponibles)/int(estacion.capacidad)
    if disp>=2/3:
        return "green"
    elif disp>=1/3:
        return "orange"
    elif 0<disp<1/3:
        return "red"
    else:
        return "gray"
        
def calcula_estadisticas(estaciones: list[EstacionSevici]) -> tuple[int, int, float, int]:
    """
    Calcula estadísticas de las estaciones.
    Parametros:
    estaciones: lista de EstacionSevici
    Devuelve:
    tupla con (total de bicicletas libres, total de capacidad, porcentaje de ocupación, total de estaciones)
    """
    tot_bicis = 0
    tot_capacidad = 0
    tot_estaciones = 0
    for e in estaciones:
        tot_bicis += e.bicicletas_disponibles
        tot_capacidad += e.capacidad
        tot_estaciones +=1
    porc_ocup = (tot_capacidad-tot_bicis)/tot_capacidad*100
    return (tot_bicis, tot_capacidad, porc_ocup, tot_estaciones)

def busca_estaciones_direccion(estaciones: list[EstacionSevici], direccion_parcial: str) -> list[EstacionSevici]:
    """
    Busca las estaciones que contengan en su dirección (subcadena, sin distinguir mayúsculas/minúsculas) la dirección parcial dada.    

    Parametros:
    estaciones: lista de EstacionSevici
    direccion_parcial: subcadena a buscar en la dirección de las estaciones

    Devuelve:
    lista de EstacionSevici que cumplen el criterio
    """
    lista = []
    for e in estaciones:
        if direccion_parcial.lower() in e.direccion.lower():
            lista.append(e)
    return lista

def busca_estaciones_con_disponibilidad(estaciones:list[EstacionSevici], min_disponibilidad: float = 0.5) -> list[EstacionSevici]:
    """
    Devuelve una lista de EstacionSevici con al menos el porcentaje mínimo de bicicletas disponible
    indicado.

    Parametros:
    estaciones: lista de EstacionSevici
    min_disponibilidad: porcentaje mínimo de bicicletas disponibles (0.0 a 1.0)
    
    Devuelve:
    lista de EstacionSevici
    """
    est_con_disp = []
    for e in estaciones:
        if e.capacidad == 0:
            disp = 0
        else:
            disp = int(e.bicicletas_disponibles)/int(e.capacidad)
        if disp > min_disponibilidad:
            est_con_disp.append(e)
    return est_con_disp

def calcula_distancia(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """
    Calcula la distancia euclídea entre dos puntos (latitud, longitud).

    Parámetros:
    p1: tupla (latitud, longitud) del primer punto
    p2: tupla (latitud, longitud) del segundo punto

    Devuelve:
    float: distancia euclídea entre los dos puntos
    """
    distancia = sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2)
    return distancia

def busca_estacion_mas_cercana(estaciones:list[EstacionSevici], punto:tuple[float, float]) -> EstacionSevici | None:
    """
    Devuelve la estación más cercana al punto dado (latitud, longitud) que tenga al menos una bicicleta disponible.
    
    Parametros:
    estaciones: lista de EstacionSevici
    punto: tupla (latitud, longitud)

    Devuelve:
    EstacionSevici más cercana con al menos una bicicleta disponible, o None si no hay ninguna.
    """ 
    est_cercana = None
    dist_cerc = 0
    for e in estaciones:
        if e.bicicletas_disponibles>=1:
            distancia_e = calcula_distancia([e.latitud,e.longitud],punto)
            if est_cercana == None or distancia_e < dist_cerc:
                dist_cerc = distancia_e
                est_cercana = e
    return est_cercana

def calcula_ruta(estaciones:list[EstacionSevici], origen:tuple[float, float], destino:tuple[float, float]) -> tuple[EstacionSevici | None, EstacionSevici | None]   :
    """
    Devuelve las estaciones más cercanas al punto de origen y destino dados, que tengan al menos una bicicleta disponible.

    Parametros: 
    estaciones: lista de EstacionSevici
    origen: tupla (latitud, longitud) del punto de origen
    destino: tupla (latitud, longitud) del punto de destino

    Devuelve:
    tupla con (estacion_origen, estacion_destino)
    """
    est_cercanas_origen = busca_estacion_mas_cercana(estaciones,origen)
    est_cercanas_destino = busca_estacion_mas_cercana(estaciones,destino)
    return est_cercanas_origen,est_cercanas_destino

