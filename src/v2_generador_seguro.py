import secrets
import string

# v2 - Versión Profesional (Segura)
# Implementación basada en estándares NIST usando 'secrets' y Fisher-Yates.
def generador():
    """
    Genera contraseñas seguras garantizando complejidad mínima y 
    usando barajado criptográfico de Fisher-Yates.
    """
    letras_minus = string.ascii_lowercase
    letras_mayus = string.ascii_uppercase
    numeros = string.digits
    simbolos = string.punctuation

    # Validación de longitud mínima para prevenir ataques de fuerza bruta
    while True:
        try:
            entrada = input('Longitud de la contraseña (mínimo 12): ')
            longitud = int(entrada)
            if longitud < 12:
                print('Por seguridad, ajustaremos la longitud a 12.')
                longitud = 12
            break
        except ValueError:
            print(f'"{entrada}" no es un número válido.')

    # Garantizamos un carácter de cada tipo para cumplir con políticas de seguridad
    obligatorios = [
        secrets.choice(letras_mayus),
        secrets.choice(letras_minus),
        secrets.choice(numeros),
        secrets.choice(simbolos),
    ]

    # Completamos la longitud deseada con una mezcla total
    restantes = longitud - len(obligatorios)
    caracteres_totales = letras_minus + letras_mayus + numeros + simbolos
    obligatorios.extend(secrets.choice(caracteres_totales) for _ in range(restantes))

    # Barajado Fisher-Yates: Elimina patrones predecibles de los caracteres obligatorios
    for i in range(len(obligatorios) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        obligatorios[i], obligatorios[j] = obligatorios[j], obligatorios[i]

    password = ''.join(obligatorios)
    print(f"Tu contraseña segura: {password}")
    return password

if __name__ == "__main__":
    generador()