# Comprobaciones visibles de M2

Comprueba cada método antes de continuar con el siguiente:

- **Nivel válido y nivel inexistente:**
  - Ante un nivel válido, el programa se abre sin problemas y comienza a ejecutarse, mostrando una salida similar a esta:

    ```text
    C:\Users\Hp1\AppData\Local\Programs\Python\Python313\Lib\site-packages\pygame\pkgdata.py:25: UserWarning: pkg_resources is deprecated as an API. See [https://setuptools.pypa.io/en/latest/pkg_resources.html](https://setuptools.pypa.io/en/latest/pkg_resources.html). The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
      from pkg_resources import resource_stream, resource_exists
    pygame 2.6.1 (SDL 2.28.4, Python 3.13.7)
    Hello from the pygame community. [https://www.pygame.org/contribute.html](https://www.pygame.org/contribute.html)
    ```

  - Ante un nivel inexistente, el programa detecta que falta el archivo y lanza el error esperado:

    ```text
    raise FileNotFoundError(f"No se encontró el archivo de nivel: {ruta}")
    FileNotFoundError: No se encontró el archivo de nivel: niveles\nivel4.txt
    ```

- **Nivel con filas de distinta longitud:**
  - Se editó de forma temporal (sin dejarlo en el repositorio) el nivel 2 añadiendo un carácter extra en la última fila. Al ejecutar el juego con ese nivel, lanza el error correspondiente:

    ```text
    raise ValueError("Todas las filas de nivel deben de tener el mismo ancho")
    ValueError: Todas las filas de nivel deben de tener el mismo ancho
    ```

- **Paleta en ambos límites de la pantalla:**
  - Probado en el nivel `demo.txt` llevando la paleta hasta ambos bordes: funciona correctamente y no se sale de los límites de la pantalla.

- **Rebote contra pared, paleta y cada tipo de bloque:**
  - Comprobado junto con la prueba anterior: la bola rebota en las paredes, rompe los bloques al impactar y aplica rebote con ángulo en la paleta.

- **Pérdida de una vida y reinicio de la bola:**
  - Comprobado en partida: al perder la bola se resta una vida (de las 3 disponibles) y se reinicia su posición.

- **Victoria al eliminar el último bloque y derrota al agotar vidas:**
  - Ambos casos funcionan: al romper todos los bloques se muestra el mensaje de victoria y la ventana se cierra tras unos segundos; al agotar las vidas se muestra el mensaje de derrota y también se cierra tras unos segundos.

- **Salida limpia con Escape y al cerrar la ventana:**
  - Comprobado durante las pruebas: la ventana se cierra limpiamente pulsando `Escape`, pulsando la `X` de la ventana o automáticamente al finalizar la partida.

Una mejora opcional no debe romper ninguno de estos casos.
