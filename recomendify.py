from constantes import *
from funciones_grafo import *
from recomendifutil import *

class Recomendify:

    def __init__(self, ruta_archivo):
        self.grafo1, self.grafo2 = generar_grafos(ruta_archivo)
        self.page_rank, self.ranking = page_rank(self.grafo2, ITERACIONES_PAGERANK)

    def camino_mas_corto(self, parametros):
        parametros = parametros.split(SEPARADOR)
        if len(parametros) != 2:
            print(ERROR_PARAMETROS_CANTIDAD)
            return
        cancion1 = parametros[0]
        cancion2 = parametros[1]
        if(not self.grafo2.existe_vertice(cancion1) or not self.grafo2.existe_vertice(cancion2)):
            print(ERROR_CANCIONES)
            return
        camino = generar_camino(self.grafo1, cancion2, cancion1)
        if not camino:
            print(ERROR_NO_RECORRIDO)
            return
        for i in range(len(camino) - 1):
            if i % 2 == 0:
                cancion_actual = camino[i]
                playlist_actual = self.grafo1.obtener_peso(camino[i], camino[i+1])[0][OFFSET_PLAYLIST_NAME]
                print(SALIDA_CANCION.format(cancion_actual, playlist_actual), end="")
            else:
                usuario_actual = camino[i]
                playlist_actual = self.grafo1.obtener_peso(camino[i], camino[i+1])[0][OFFSET_PLAYLIST_NAME]
                print(SALIDA_USUARIO.format(usuario_actual, playlist_actual), end="")
        print(camino[len(camino)- 1])

    def canciones_mas_importantes(self, parametros):
        if len(parametros) != 1:
            print(ERROR_PARAMETROS_CANTIDAD)
            return
        if not parametros.isnumeric():
            print(ERROR_NO_NUMERICO)
            return
        
        canciones = ""
        for i in range(int(parametros)):
            canciones += f"{self.ranking[i]}; "
        print(canciones[:-2]) # Slice para que que no este el ultimo '; '

    def recomendacion(self, comando):
        #Parsear comando                #Parametro[0] = canciones/usuarios      Parametro[1] = cantidad de recomendaciones
        comando = comando.split(" ")
        if len(comando) == 0:
            print(ERROR_PARAMETROS_NULO)
            return
        if len(comando) < 3:
            print(ERROR_PARAMETROS_CANTIDAD)
            return

        if comando[0] != CANCIONES and comando[1] != USUARIOS:
            print(ERROR_PARAMETROS_INCORRECTOS)
            return

        if not comando[1].isnumeric():
            print(ERROR_NO_NUMERICO)
            return
        largo_comandos = len(comando[0]) + len(comando[1])
        modo_algoritmo = comando[0]
        cantidad_recomendaciones = int(comando[1])
        comando = " ".join(comando)
        comando = comando[largo_comandos + 2:]
        canciones = comando.split(SEPARADOR)
        #----------------------------------------------------------------------
        RANDOM_WALKS = 10
        LEN_WALKS = cantidad_recomendaciones * 2    #Por cada cancion que busque va a pasar por un usuario
        page_rank_per = page_rank_personalizado(self.grafo1, canciones,RANDOM_WALKS, LEN_WALKS)
        
        ranking = sorted([item for item in page_rank_per.keys if self.grafo2.existe_vertice(x)], keys = page_rank.get(), reverse = True)
        print(ranking)

    def ciclo_de_n_canciones(self, parametros):
        parametros = parametros.split(" ")
        if len(parametros) < 2:
            print(ERROR_PARAMETROS_CANTIDAD)
            return
        n = parametros[0]
        if not n.isnumeric():
            print(ERROR_NO_NUMERICO)
            return
        cancion = " ".join(parametros[1:])
        parametros = (n, cancion)
        if len(parametros) != 2:
            print(ERROR_PARAMETROS_CANTIDAD)
            return
        if not self.grafo2.existe_vertice(parametros[1]):
            print(ERROR_NO_EXISTE_CANCION)
            return
        lista = ciclo_backtracking(self.grafo2, int(parametros[0]), parametros[1])
        if not lista:
            print(ERROR_NO_CICLO)
            return
        print(lista)

    def todas_en_rango(self, parametros):
        parametros = parametros.split(" ")
        if len(parametros) < 2:
            print(ERROR_PARAMETROS_CANTIDAD)
            return
        n = parametros[0]
        if not n.isnumeric():
            print(ERROR_NO_NUMERICO)
            return
        cancion = " ".join(parametros[1:])
        parametros = (n, cancion)
        if len(parametros) != 2:
            print(ERROR_PARAMETROS_CANTIDAD)
            return
        if not self.grafo2.existe_vertice(parametros[1]):
            print(ERROR_NO_EXISTE_CANCION)
            return
        orden = bfs_parcial_orden(self.grafo2, parametros[1], int(n))
        canciones_a_n_distancia = []
        for v in orden:
            if orden[v] == int(n):
                canciones_a_n_distancia.append(v)
        print(len(canciones_a_n_distancia))

    def coeficiente_de_clustering(self, parametros):
        pass


