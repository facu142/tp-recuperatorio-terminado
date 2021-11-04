import random
from main import FORMATO


letras = 'abcdefghijklmnopqrstuvwxyz'
generos = 'Balada', 'Pop', 'Rock', 'Folclore', 'Electrónica', 'Otros'
idiomas = 'Español', 'Inglés', 'Francés', 'Portugués', 'Otros'


class Tema:
	def __init__(self, titulo, genero, idioma):
		self.titulo = titulo
		self.genero = genero
		self.idioma = idioma

	def __str__(self):
		return FORMATO.format(self.titulo, generos[self.genero], idiomas[self.idioma])


def crear_tema_aleatorio():
	titulo = random.choice(letras)
	genero = random.randint(0, 5)
	idioma = random.randint(0, 4)

	return Tema(titulo, genero, idioma)
