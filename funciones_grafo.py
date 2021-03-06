from collections import deque
import random

def _dfs(grafo, v, visitados, padres, orden):
    visitados.add(v)
    a = {}
    for w in grafo.obtener_adyacentes(v).keys():
        padres[w] = v
        orden[w] = orden[v] + 1
        _dfs(grafo, w, visitados, padres, orden)

def dfs(grafo, id_origen):
    padres = {}
    orden = {}
    visitados = set()
    _dfs(grafo, id_origen, visitados, padres, orden)
    for v in grafo.obtener_vertices():
        if v not in visitados:
           _dfs(grafo, v, visitados, padres, orden) 
    return padres, orden

def bfs(grafo, id_origen):
    padres = {}
    orden = {}
    visitados = set()
    padres[id_origen] = None
    orden[id_origen] = 0
    visitados.add(id_origen)
    q = deque()
    q.appendleft(id_origen)
    while len(q) > 0:
        v = q.pop()
        for w in grafo.obtener_adyacentes(v).keys():
            if w not in visitados:
                padres[w] = v
                orden[w] = orden[v] + 1
                visitados.add(w)
                q.appendleft(w)
    return padres, orden

def bfs_parcial_padres(grafo, id_origen, id_destino):
    padres = {}
    visitados = set()
    padres[id_origen] = None
    visitados.add(id_origen)
    cola = deque()
    cola.appendleft(id_origen)
    while len(cola) > 0:
        vertice = cola.pop()
        for adyacente in grafo.obtener_adyacentes(vertice).keys():
            if adyacente not in visitados:
                padres[adyacente] = vertice
                visitados.add(adyacente)
                cola.appendleft(adyacente)
                if adyacente == id_destino:
                    return padres
    return None

def bfs_parcial_orden(grafo, id_origen, n):
    orden = {}
    visitados = set()
    orden[id_origen] = 0
    visitados.add(id_origen)
    cola = deque()
    cola.appendleft(id_origen)
    while len(cola) > 0:
        vertice = cola.pop()
        for adyacente in grafo.obtener_adyacentes(vertice).keys():
            if adyacente not in visitados:
                orden[adyacente] = orden[vertice] + 1
                if orden[adyacente] > n:
                    return orden
                visitados.add(adyacente)
                cola.appendleft(adyacente)
    return orden

def _generar_camino(camino, padres, padre):
    if not padre:
        return
    camino.append(padre)
    _generar_camino(camino, padres, padres[padre])

def generar_camino(grafo, vertice1, vertice2):
    padres = bfs_parcial_padres(grafo, vertice1, vertice2)
    if not padres:
        return None
    camino = []
    _generar_camino(camino, padres, vertice2)
    return camino

def convergencia(dic1,dic2):
    diferencias = 0
    lista1 = sorted([item for item in dic1.keys()], key = dic1.get, reverse = True)
    lista2 = sorted([item for item in dic2.keys()], key = dic2.get, reverse = True)
    for i in range(len(lista1)):
        diferencias += lista1[i] != lista2[i]
    return diferencias == 0

def limpiar_diccionarios(dic1, dic2):
    dic1.clear()
    for key, value in dic2.items():
        dic1[key] = value
    dic2.clear()


def _page_rank_vertice(grafo, vertice, page_rank):
    
    d = 0.85
    N = grafo.obtener_cantidad_vertices()

    sumatoria = 0
    for adyacente in grafo.obtener_adyacentes(vertice):
        sumatoria += page_rank[adyacente] / grafo.obtener_cantidad_adyacentes(adyacente)
    
    return ((1.0 - d) / N ) + (d * sumatoria)

def page_rank(grafo):
    page_rank_anterior = {}
    page_rank_nuevo = {}
    #Inicializar todos los pageranks en 1 / cant_vertices
    for vertice in grafo.obtener_vertices():
        page_rank_anterior[vertice] = 1 / grafo.obtener_cantidad_vertices()
    
    convergen = False
    while not convergen:
        for vertice in grafo.obtener_vertices():
            page_rank_nuevo[vertice] = _page_rank_vertice(grafo, vertice, page_rank_anterior)
        convergen = convergencia(page_rank_anterior, page_rank_nuevo)
        limpiar_diccionarios(page_rank_anterior, page_rank_nuevo)
    
    return page_rank_anterior


def _page_rank_personalizado_vertice(grafo, page_rank, vertice_anterior, vertice_actual):
    pr_anterior = page_rank.get(vertice_anterior, 1)
    return page_rank.get(vertice_actual, 0) + pr_anterior / grafo.obtener_cantidad_adyacentes(vertice_anterior)

def page_rank_personalizado(grafo, vertices, rw_cantidad, rw_largo, tp_probabilidad): # rw = random_walks
    page_rank = {}
    for vertice in vertices:
        actual = random.choice(list(grafo.obtener_adyacentes(vertice)))
        anterior = vertice
        #Hacer rw_cantidad numero de random walks
        for i in range (rw_cantidad):
            #Saltar rw_largo de veces de un vertice a otro adyacente aleatoreo
            for j in range(rw_largo):
                page_rank[actual] = _page_rank_personalizado_vertice(grafo, page_rank, anterior, actual)
                anterior = actual
                actual = random.choice(list(grafo.obtener_adyacentes(actual)))
    return page_rank

def _ciclo_backtracking(grafo, n, n_max, vertice_actual, vertice_buscado, visitados, orden):
    if n > n_max:
        return False, None
    if vertice_actual == vertice_buscado and n == n_max:
        return True, [vertice_actual]

    for ad in grafo.obtener_adyacentes(vertice_actual):
        if ad == vertice_buscado and n != n_max - 1:
            continue
        if orden[ad] > (n_max - n):
            continue
        if ad not in visitados:
            visitados.add(ad)
            resultado, lista = _ciclo_backtracking(grafo, n+1, n_max, ad, vertice_buscado, visitados, orden)
            if resultado:
                lista.append(vertice_actual)
                return resultado, lista
            else:
                visitados.remove(ad)
    return False, None

def ciclo_backtracking(grafo, n, vertice):
    _, orden = bfs(grafo, vertice)
    visitados = set()
    resultado, lista = _ciclo_backtracking(grafo, 0, n, vertice, vertice, visitados, orden)
    if resultado:
        lista.reverse()
    return lista

def clustering(grafo, vertice):   
    if grafo.obtener_cantidad_adyacentes(vertice) < 2:
        return 0
    adyacentes_adyacentes = 0
    for v in grafo.obtener_adyacentes(vertice).keys():
        for z in grafo.obtener_adyacentes(vertice).keys():
            if grafo.es_adyacente(v, z):
                adyacentes_adyacentes += 1
    ci = adyacentes_adyacentes
    ki = grafo.obtener_cantidad_adyacentes(vertice)
    return round(ci / (ki * (ki - 1)), 3)