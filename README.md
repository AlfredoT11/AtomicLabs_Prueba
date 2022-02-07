# AtomicLabs_Prueba
Este repositorio contiene el código fuente de la prueba de programación para becario Backend para Atomic Labs.

## Instalación y modo de uso
Para ejecutar este programa se deben instalar los paquetes especificados en requirements.txt, una vez instalados se debe ejecutar el script model_visualization.py

Se utilizó Python 3.9.9 para el desarrollo de este programa.

## Descripción del sistema 
Se tiene una oficina llena de trabajadores la cuál es invadida por 2 zombies.
Los zombies al ingresar se mueven 4 casillas en cada iteración, no obstante, nunca regresan a la misma casilla anterior. Cuando un zombie tiene a su lado un humano sin infectar lo infecta. Después de 2 iteraciones de espera, el humano infectado se convierte en zombie.

El objetivo de los trabajadores es escapar de la oficina por la salida.

## Explicación de la solución
Para llegar a la solución utilicé un modelo basado en agentes (MBA), cada trabajador, zombie y pared dentro del espacio es un agente. La decisión de utilizar un MBA para resolver el problema es debido a la relación tan natural que se tiene de tener diferentes entidades que tienen un objetivo en específico. En este caso se tienen 3 entidades diferentes; trabajador, zombie y pared. El objetivo de un trabajador es escapar de la oficina, el del zombie es infectar más humanos y el de la pared es bloquear el camino. Además de que cada uno tiene un objetivo muy específico, cada agente tiene conocimiente sobre el entorno, este conocimiento les permite tomar decisiones adecuadas para cumplir su objetivo. Por supuesto, para implementar un MBA se debe usar una herramienta adecuada, para este caso seleccioné el paquete Mesa de Python, este paquete permite crear este tipo de modelos de forma sencilla ya que ofrece diversa fncionalidad para que el desarrollador únicamente se preocupe por el código específico de cada agente para que alcance su objetivo.

Decidí dividir la oficina en 5 zonas diferentes, dependiendo de la zona el trabajador guiará su movimiento de forma diferente. Cada trabajador selecciona la siguiente casilla de forma aleatoria, sin embargo, existe una mayor probabilidad de movimiendo en cierta dirección en función de la zona y la distancia a ciertas casillas.

En la zona 1 existen 3 salidas para pasar a la siguiente zona, el trabajador determina la salida más cercana a partir de su distancia en el eje x.
En la zona 2 únicamente existe una salida para la siguiente zona.
En la zona 3 existen 2 salidas para la siguiente zona, al igual que la zona 1, el trabajador determina la salida más cercana, sin embargo, aquí sí toma en cuenta la distancia de los ejes x e y.
En la zona 4 existen 2 salidas para la siguiente zona. El trabajador determina la salida más cercana para modificar sus probabilidades de movimiento.
La zona 5 es la que cuenta con la salida general de la oficina, por lo que el movimiento siempre estará cargado a esas casillas.

Las probabilides de movimiento funcionan de la siguiente manera:

El trabajador determina una casilla objetivo dependiendo de la zona en la que se encuentre, una vez determinada esta casilla se calcula la diferencia entre la casilla objetivo y la posición en ese momento del trabajador. Si la diferencia de la coordenada x es positiva, es más probable que el trabajador vaya a la derecha, en caso contrario, será más probable que vaya a la izquierda. Si la diferencia de la coordenada y es positiva, es más probable que el trabajador vaya hacia arriba, en caso contrario es más probable que se mueva hacia abajo.

Por supuesto, estas condiciones se pueden combinar, por ejemplo, si se tiene una diferencia positiva no solo es más probable que el trabajador se mueva hacia la derecha y hacia arriba, si no que también es más probable que se mueva en diagonal hacia arriba y la derecha. 

