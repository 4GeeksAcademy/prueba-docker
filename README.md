# Comandos básicos de Docker

Docker permite ejecutar aplicaciones en contenedores con sus dependencias.

- **Imagen:** plantilla usada para crear contenedores.
- **Contenedor:** instancia de una imagen; puede estar en ejecución o detenida.
- **Dockerfile:** archivo con las instrucciones para construir una imagen.
- **Volumen:** almacenamiento que puede conservar datos aunque elimines el contenedor.

En los comandos, sustituye los valores entre `< >` por nombres o identificadores reales, sin escribir los signos.

## Consultar Docker

| Comando | Qué hace |
| --- | --- |
| `docker --version` | Muestra la versión instalada del cliente de Docker. |
| `docker info` | Muestra información del motor de Docker y sus recursos. Requiere que el motor esté disponible. |
| `docker <comando> --help` | Muestra las opciones de un comando, por ejemplo `docker run --help`. |

## Gestionar imágenes

| Comando | Qué hace |
| --- | --- |
| `docker pull nginx:alpine` | Descarga la imagen `nginx` con la etiqueta `alpine` desde Docker Hub. |
| `docker images` | Lista las imágenes locales, sus etiquetas, identificadores y tamaños. |
| `docker build -t prueba-frontend ./frontend` | Construye la imagen `prueba-frontend` usando el Dockerfile y los archivos de `frontend`. Ejecuta este ejemplo desde la raíz del proyecto. |
| `docker rmi <imagen>` | Elimina una imagen local. Puede fallar si algún contenedor, incluso detenido, la utiliza. |

En `docker build`, `-t` asigna un nombre y una etiqueta a la imagen. Si omites la etiqueta, se utiliza `latest`. La ruta final es el **contexto de construcción**: los archivos disponibles para instrucciones como `COPY`.

## Crear y listar contenedores

Para ejecutar el frontend después de construir su imagen:

```bash
docker run -d --name web -p 8080:80 prueba-frontend
```

- `docker run`: crea e inicia un contenedor nuevo a partir de una imagen.
- `-d`: lo deja ejecutándose en segundo plano.
- `--name web`: asigna el nombre `web` al contenedor.
- `-p 8080:80`: conecta el puerto `8080` del host con el puerto `80` del contenedor.
- `prueba-frontend`: imagen que se utilizará.

Accede a `http://localhost:8080` desde el host de Docker. En Codespaces, utiliza la URL del puerto `8080` en la pestaña **Ports/Puertos** de VS Code.

> `EXPOSE 80` en el Dockerfile documenta el puerto del servicio, pero no lo publica. Para acceder desde fuera del contenedor necesitas `-p`.

| Comando | Qué hace |
| --- | --- |
| `docker ps` | Lista los contenedores en ejecución y sus puertos publicados. |
| `docker ps -a` | Lista todos los contenedores, incluidos los detenidos. |
| `docker run --rm nginx:alpine` | Crea un contenedor y lo elimina automáticamente cuando termina. Este ejemplo queda en primer plano; puedes detenerlo con `Ctrl+C`. |

## Inspeccionar un contenedor

| Comando | Qué hace |
| --- | --- |
| `docker logs web` | Muestra la salida estándar y los errores registrados por el contenedor. |
| `docker logs -f web` | Sigue los nuevos mensajes en tiempo real. `Ctrl+C` deja de seguirlos sin detener el contenedor. |
| `docker exec -it web sh` | Abre una terminal dentro del contenedor en ejecución. `-i` mantiene la entrada abierta y `-t` asigna una terminal. |
| `docker exec web ls /usr/share/nginx/html` | Ejecuta un comando dentro del contenedor sin abrir una sesión interactiva. |
| `docker inspect web` | Muestra detalles en JSON, como configuración, redes y montajes. |
| `docker stats` | Muestra en tiempo real el consumo de CPU, memoria y otros recursos de los contenedores en ejecución. Sal con `Ctrl+C`. |

Para salir de la terminal abierta con `docker exec`, escribe `exit`. Esto no detiene el proceso principal del contenedor. La imagen `nginx:alpine` incluye `sh`; no todas las imágenes incluyen `bash`.

## Detener, iniciar y eliminar

| Comando | Qué hace |
| --- | --- |
| `docker stop web` | Solicita detener el contenedor y fuerza su parada si no termina dentro del tiempo de espera. No lo elimina. |
| `docker start web` | Inicia de nuevo el mismo contenedor detenido, conservando su configuración. |
| `docker restart web` | Detiene y vuelve a iniciar el contenedor. |
| `docker rm web` | Elimina un contenedor detenido. No elimina su imagen. |
| `docker rm -f web` | Fuerza la parada y eliminación de un contenedor, aunque esté en ejecución. Úsalo con cuidado. |

`docker run` crea un contenedor nuevo; `docker start` reutiliza uno existente. Si el nombre `web` ya está ocupado, inicia ese contenedor o elimínalo antes de crear otro con el mismo nombre.

> Al eliminar un contenedor se pierde lo guardado en su capa de escritura. Los datos guardados en volúmenes o carpetas montadas tienen un ciclo de vida separado.

## Volúmenes y redes

| Comando | Qué hace |
| --- | --- |
| `docker volume create datos` | Crea un volumen llamado `datos`. |
| `docker volume ls` | Lista los volúmenes existentes. |
| `docker volume inspect datos` | Muestra la información del volumen. |
| `docker volume rm datos` | Elimina el volumen y sus datos. No puede estar en uso por un contenedor. |
| `docker network ls` | Lista las redes de Docker. |
| `docker network create mi-red` | Crea una red; puedes conectar nuevos contenedores usando `docker run --network mi-red ...`. |
| `docker network inspect mi-red` | Muestra la configuración de la red y sus contenedores conectados. |
| `docker network rm mi-red` | Elimina la red si no tiene contenedores conectados. |

Para montar un volumen, añade `-v datos:/ruta/dentro/del/contenedor` a `docker run`. La ruta debe corresponder a la carpeta donde la aplicación guarda sus datos.

## Limpiar recursos

| Comando | Qué hace |
| --- | --- |
| `docker system df` | Muestra el espacio utilizado por imágenes, contenedores, volúmenes y caché de construcción. |
| `docker container prune` | Elimina todos los contenedores detenidos. |
| `docker image prune` | Elimina imágenes sin etiqueta que no están referenciadas por contenedores. |
| `docker system prune` | Elimina contenedores detenidos, redes sin uso, imágenes sin etiqueta no utilizadas y caché de construcción no utilizada. No elimina volúmenes por defecto. |

> Los comandos `prune` solicitan confirmación. Revisa lo que vas a eliminar: los contenedores detenidos también pueden contener datos importantes. Evita añadir `-f`, que omite la confirmación, mientras estás aprendiendo.

## Ejemplo completo del frontend

Ejecuta estos comandos desde la raíz del proyecto. El nombre `web` debe estar libre:

```bash
docker build -t prueba-frontend ./frontend
docker run -d --name web -p 8080:80 prueba-frontend
docker ps
docker logs web
docker exec -it web sh
```

Después de salir de la terminal del contenedor con `exit`, puedes detenerlo y eliminar los recursos creados:

```bash
docker stop web
docker rm web
docker rmi prueba-frontend
```

Si modificas el HTML local, debes reconstruir la imagen y recrear el contenedor para ver los cambios: `COPY` copia los archivos durante la construcción, no los sincroniza mientras el contenedor está funcionando.