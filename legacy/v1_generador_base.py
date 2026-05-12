import random

# v1 - Versión Educativa (Insegura)
# Este script fue el punto de partida para entender la lógica de bucles.
# ADVERTENCIA: Usa 'random', por lo que no es apto para uso real.
def generador():
  caracter = '@#$_&-+()/*:;!?~`£¢€¥^°%abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ1234567890'
  acumulador = ''
  while True:
    try:
      entrada = int(input('Longitud de la contraseña (mayor a 9 caracteres): '))
      if entrada <= 9:
        print('Esa no es una longitud válida')
        continue
      break
    except ValueError:
      print('Eso no parece ser un número válido')
      continue
  for i in range(0, entrada):
      acumulador += random.choice(caracter)
  print('Su contraseña generada:', acumulador)  
generador()