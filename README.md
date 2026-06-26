# PassForge — Generador de contraseñas (aprendizaje + versión segura)

Este repositorio empezó como un proyecto básico para practicar Python (Coursera): un generador de contraseñas por consola.  
Con el tiempo, lo revisé desde el punto de vista de seguridad y encontré varios problemas en la **primera versión** (v1).  
Luego implementé una **versión mejorada** (v2) usando `secrets` y una política mínima de complejidad.

> **Importante:** La v1 sirve como ejemplo educativo de lo que *NO* debe usarse para generar contraseñas reales.  
> Si necesitas contraseñas para uso real, usa la v2 (o una variante equivalente).

---

## Contenido
- [Resumen rápido](#resumen-rápido)
- [v1 (original): análisis y vulnerabilidades](#v1-original-análisis-y-vulnerabilidades)
  - [1) `random` no es criptográficamente seguro](#1-random-no-es-criptográficamente-seguro)
  - [2) No hay política de complejidad](#2-no-hay-política-de-complejidad)
  - [3) “Más caracteres” no arregla el problema](#3-más-caracteres-no-arregla-el-problema)
  - [4) Errores de diseño menores (calidad/UX)](#4-errores-de-diseño-menores-calidadux)
- [v2 (mejorada): por qué es más segura](#v2-mejorada-por-qué-es-más-segura)
  - [1) `secrets` (CSPRNG)](#1-secrets-csprng)
  - [2) Longitud mínima real](#2-longitud-mínima-real)
  - [3) Reglas de complejidad](#3-reglas-de-complejidad)
- [Comparación v1 vs v2](#comparación-v1-vs-v2)
- [Ejemplos de ejecución](#ejemplos-de-ejecución)
- [Próximos pasos y mejoras](#próximos-pasos-y-mejoras)
- [Licencia](#licencia)

---

## Resumen rápido

**Problema principal en v1:** usa `random` (Mersenne Twister), un generador pseudoaleatorio diseñado para simulación, no para seguridad.  
En seguridad, “parece aleatorio” no es suficiente: importa que sea resistente ante un adversario.

**v2 soluciona lo principal** al usar `secrets` y añade reglas mínimas para evitar contraseñas débiles.

---

## v1 (original): análisis y vulnerabilidades

Esta fue la idea inicial (simplificada):

```python
import random

def generador():
  caracter = '@#$_&-+()/*:;!?~`£¢€¥^°%abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ1234567890'
  acumulador = ''
  entrada = int(input('Longitud de la contraseña (mayor a 9 caracteres): '))
  for i in range(0, entrada):
      acumulador += random.choice(caracter)
  print('Su contraseña generada:', acumulador)

generador()
```

### 1) `random` no es criptográficamente seguro

- `random` en Python está basado en **Mersenne Twister**, excelente para simulaciones, pero **no** para criptografía.
- En términos prácticos: un PRNG no criptográfico puede ser **predecible** si un atacante llega a conocer o reconstruir su estado interno (por observación suficiente de salidas, o por condiciones de inicialización/entorno, o por acceso parcial al proceso).
- Por eso la propia documentación de Python recomienda `secrets` para contraseñas y tokens.

**Qué significa “no apto”:**
- No es que “siempre sea trivial romperlo”, sino que **no cumple el estándar** que se exige para contraseñas en entornos reales.
- En seguridad, si algo no es CSPRNG, se considera un riesgo.

> Conclusión: aunque genere cadenas “que se ven random”, **no es una base correcta para contraseñas**.

### 2) No hay política de complejidad

La v1 puede generar contraseñas como:
- solo números,
- solo letras minúsculas,
- sin símbolos,
- sin mezcla de clases.

Aunque muchas organizaciones ya no exigen “complejidad” estricta si la longitud es grande, en contraseñas cortas/medias sí ayuda a evitar resultados débiles por azar.

Ejemplo (posible en v1 con longitud 10):
- `aaaaaaaaaa`
- `1234567890`
- `abcdefghij`

No es lo típico, pero **puede ocurrir** y no hay nada que lo impida.

### 3) “Más caracteres” no arregla el problema

En v1 hay muchos caracteres permitidos. Eso aumenta el espacio de búsqueda, sí.  
Pero el problema principal no es el tamaño del alfabeto: es el **tipo de aleatoriedad**.

Si la aleatoriedad no es criptográficamente segura, aumentar el alfabeto **no convierte** el sistema en seguro.

### 4) Errores de diseño menores (calidad/UX)

No son “vulnerabilidades” graves, pero sí detalles mejorables:

- Límite mínimo: el mensaje dice “mayor a 9”, pero el criterio es `<= 9`, o sea mínimo real 10.
- Se imprime la contraseña directamente; en algunos entornos esto puede quedar en historial/logs (depende de dónde se ejecute).
- No hay estructura para reutilizar el generador desde otro módulo (está “pegado” al `input()` y al `print()`).

---

## v2 (mejorada): por qué es más segura

Versión mejorada (la idea principal):

```python
import secrets
import string

def generador():
    letras = string.ascii_letters
    numeros = string.digits
    simbolos = string.punctuation
    caracteres = letras + numeros + simbolos

    # mínimo 12
    # genera usando secrets
    # garantiza presencia de mayús, minús, número y símbolo
```

### 1) `secrets` (CSPRNG)

- `secrets` usa una fuente de aleatoriedad adecuada para seguridad (CSPRNG), alimentada por el sistema operativo.
- Está diseñada específicamente para:
  - contraseñas
  - tokens
  - credenciales temporales
  - valores que no deben ser predecibles

**Este es el cambio más importante del proyecto.**

### 2) Longitud mínima real

- v2 fuerza un mínimo (por ejemplo 12).
- Esto eleva muchísimo la resistencia contra fuerza bruta, incluso si alguien intenta adivinar.

### 3) Reglas de complejidad

v2 comprueba que la contraseña tenga:
- al menos una mayúscula
- al menos una minúscula
- al menos un número
- al menos un símbolo

Esto evita resultados “accidentalmente débiles”.

> Nota: Para contraseñas muy largas, la complejidad importa menos.  
> Para longitudes moderadas (12–16), sigue siendo una buena regla práctica.

---

## Comparación v1 vs v2

| Aspecto | v1 (original) | v2 (mejorada) |
|---|---|---|
| RNG | `random` (no CSPRNG) | `secrets` (CSPRNG) |
| Uso recomendado | Simulación/juegos | Tokens/contraseñas |
| Longitud mínima | 10 (por validación) | 12 (o la que definas) |
| Complejidad | No garantiza mezcla | Garantiza mayús/minús/número/símbolo |
| Probabilidad de contraseñas “pobres” | Existe | Mucho menor (por validación) |

---

## Ejemplos de ejecución

### v1 (original)

Entrada:
- Longitud: `10`

Salida (ejemplo):
- `Su contraseña generada: aF3p0z...` *(ejemplo)*

Problema: aunque “se vea aleatoria”, el origen (`random`) **no está diseñado** para resistir ataques reales.

### v2 (mejorada)

Entrada:
- Longitud: `8`

Salida:
- `Por seguridad, ajustaremos la longitud a 12.`
- `Tu contraseña: ...` *(ejemplo)*

Ventaja: usa `secrets` y cumple reglas mínimas.

---

## Próximos pasos y mejoras

Este proyecto es una base para seguir practicando Python. Algunas funcionalidades que me gustaría añadir más adelante son:

* **Filtro de caracteres:** Permitir al usuario elegir si quiere excluir ciertos símbolos que a veces dan problemas en algunas webs (como las comillas o barras).
* **Exportación a archivo:** Añadir una opción para guardar la contraseña generada de forma local.
* **Analizador de fuerza:** Integrar un módulo que calcule el tiempo estimado de crackeo de la contraseña generada.

---

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE). 

Puedes usarlo, modificarlo y distribuirlo libremente, siempre que mantengas el aviso de copyright y la nota de licencia. ¡Espero que te sirva para aprender tanto como me sirvió a mí!