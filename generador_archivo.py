import pickle

NOMBRE_ARCHIVO = 'musica.csv'

from registro import *


def crear_archivo_temas(nombre_archivo, n):
	archivo = open(nombre_archivo, 'wb')

	for i in range(n):
		nuevo_tema = crear_tema_aleatorio()
		pickle.dump(nuevo_tema, archivo)

	archivo.close()
	print(f'Se ha creado el archivo {nombre_archivo} con {n} temas')


def principal():
	n = int(input('Candidad de temas a cargar: '))
	crear_archivo_temas(NOMBRE_ARCHIVO, n)


if __name__ == '__main__':
	principal()
