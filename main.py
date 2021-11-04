import os
import pickle

from registro import *

NOMBRE_ARCHIVO = 'musica.csv'
FORMATO = '{:<15} | {:^12} | {:^10}'


def mostrar_menu():
	print('******** MENU DE OPCIONES ********')
	print('1- Generar vector de registros')
	print('2- Generar lista de un idioma')
	print('3- Determinar la cantidad de temas por género y por idioma')
	print('4- Determinar la cantidad de temas musicales para el género g')
	print('5- Buscar en el vector original un tema musical con el título x')
	print('6- Generar “MusicaIdiomax.dat')
	print('7- Leer “MusicaIdiomaX.dat”')
	print('8- Salir\n')


def add_in_order_titulo(temas, tema):
	izq = 0
	der = len(temas) - 1
	pos = len(temas)

	while izq <= der:
		c = (izq + der) // 2
		if temas[c].titulo == tema.titulo:
			pos = c
			break
		if tema.titulo < temas[c].titulo:
			der = c - 1
		else:
			izq = c + 1

	if izq > der:
		pos = izq

	temas[pos:pos] = [tema]


def cargar_temas_a_vector():
	temas = []

	# La existencia del archivo esta validada en principal()

	tam = os.path.getsize(NOMBRE_ARCHIVO)
	archivo = open(NOMBRE_ARCHIVO, 'rb')

	while archivo.tell() < tam:
		tema = pickle.load(archivo)
		add_in_order_titulo(temas, tema)

	return temas


def mostrar_temas(temas):
	print('\n************ Listado de temas ************\n')
	print(FORMATO.format('Titulo', 'Genero', 'Idioma'))
	for tema in temas:
		print(tema)
	print()


def generar_lista_idioma_i(temas, n, idioma):
	temas_idioma_i = []
	cont = 0

	for tema in temas:
		if len(temas_idioma_i) == n:
			break
		if tema.idioma == idioma:
			cont += 1
			temas_idioma_i.append(tema)

	return temas_idioma_i


def crear_matriz(filas, columnas):
	return [[0] * filas for f in range(columnas)]


def contar_temas_por_genero_idioma(mat, temas):
	for tema in temas:
		mat[tema.genero][tema.idioma] += 1


def mostrar_matriz(mat):
	print('\n***** Cantidad por genero e idioma *****')
	for i in range(len(mat)):
		for j in range(len(mat[0])):
			if mat[i][j] != 0:
				print(f'Genero {generos[i]}, Idioma {idiomas[j]} => {mat[i][j]}')

	print()


def contar_temas_genero_g(mat, g):
	cont = 0
	for casillero in mat[g]:
		cont += casillero

	print(f'\nTemas para el genero {generos[g]}: {cont}\n')


def buscar_por_titulo(temas, x_titulo):
	izq = 0
	der = len(temas) - 1

	while izq <= der:
		c = (izq + der) // 2
		if x_titulo == temas[c].titulo:
			return temas[c]
		if x_titulo < temas[c].titulo:
			der = c - 1
		else:
			izq = c + 1
	return -1


def generar_archivo_idioma(temas, i):
	nombre_archivo = f'MusicaIdioma{i}.dat'
	archivo = open(nombre_archivo, 'wb')
	cont = 0

	for tema in temas:
		if tema.idioma == i:
			pickle.dump(tema, archivo)
			cont += 1

	archivo.close()
	print(f'Se ha creado el archivo {nombre_archivo} con {cont} registros\n')


def leer_archivo_idioma(i, temas):
	nombre_archivo = f'MusicaIdioma{i}.dat'

	if os.path.exists(nombre_archivo):
		archivo = open(nombre_archivo, 'rb')
		tam = os.path.getsize(nombre_archivo)

		print(f'\n******* Contenido de "{nombre_archivo}" ********')
		print(FORMATO.format('Titulo', 'Genero', 'Idioma'))

		while archivo.tell() < tam:
			tema = pickle.load(archivo)
			print(tema)
		print()

	else:
		print(f'\nNo existia el archivo {nombre_archivo}. Se procede a crearlo..\n')
		generar_archivo_idioma(temas, i)
		leer_archivo_idioma(i, temas=None)


def principal():
	temas = []
	mat = None
	mostrar_menu()
	opc = int(input('Ingrese la opcion: '))

	while opc != 8:

		if not os.path.exists(NOMBRE_ARCHIVO):
			print(f'\nDebe crear el archivo {NOMBRE_ARCHIVO} primero, ejecutando "generador archivos.py"')
			break

		if opc == 1:
			temas = cargar_temas_a_vector()
			mostrar_temas(temas)

		elif opc == 2:
			i = int(input('Idioma: (0-Español, 1: Inglés, 2: Francés, 3: Portugués, 4:Otros) '))
			n = int(input(f'Cantidad de temas a cargar del idioma {idiomas[i]}: '))

			temas_idioma_i = generar_lista_idioma_i(temas, n, idioma=i)
			cant_cargada = len(temas_idioma_i)

			if cant_cargada == 0:
				print(f'\nNo se encontraron temas del idioma {idiomas[i]}\n')
			elif cant_cargada == n:
				print(f'\nSe han cargado los {n} temas a la lista\n')
				mostrar_temas(temas_idioma_i)
			elif cant_cargada < n:
				print(f'\nLa cantidad de temas disponibles son insuficientes, se han cargado {cant_cargada} temas\n')
				mostrar_temas(temas_idioma_i)

		elif opc == 3:
			mat = crear_matriz(filas=5, columnas=4)
			contar_temas_por_genero_idioma(mat, temas)
			mostrar_matriz(mat)

		elif opc == 4:
			if mat:
				g = int(input(
					'Ingrese un genero a contar: (0-Balada, 1-Pop, 2-Rock, 3-Folclore, 4-Electrónica, 5-Otros.) '))
				contar_temas_genero_g(mat, g)
			else:
				print('\nDebe crear la matriz primero (opcion 3)\n')

		elif opc == 5:
			x = input('Titulo a buscar: ')
			tema_encontrado = buscar_por_titulo(temas, x)

			if tema_encontrado != -1:
				print(f'\nSe ha encontrado un tema con el nombre {x}\n')
				print(FORMATO.format('Titulo', 'Genero', 'Idioma'))
				print(tema_encontrado)
				print()
			else:
				print(f'\nNo se ha encontrado un tema con el nombre {x}\n')

		elif opc == 6:
			print('\nGenerar Archivo de un idioma..\n')
			i = int(input('Ingrese el idioma: 0-Español, 1: Inglés, 2: Francés, 3: Portugués, 4:Otros.'))

			generar_archivo_idioma(temas, i)
		elif opc == 7:
			print('\nLeer o generar (si no existe) Archivo de un idioma..\n')
			i = int(input('Ingrese el Idioma: 0-Español, 1: Inglés, 2: Francés, 3: Portugués, 4:Otros.'))

			leer_archivo_idioma(i, temas)

		else:
			print('\nIngrese una opcion correcta\n')

		mostrar_menu()
		opc = int(input('Ingrese la opcion: '))


if __name__ == '__main__':
	print('\nBienvenido al Sistema de Gestión de Listas Musicales\n')
	principal()
	print('\nPrograma finalizado')
