# tasks

## Descripción

Proyecto de prueba para aplicar al cargo de Desarrollador Backend en Elenas. \
Puedes ver un Demo en vivo del proyecto en [3.138.170.182/es/swagger/](http://3.138.170.182/es/swagger/).

## Requerimientos / Características

* Los usuarios se deben autenticar.
* Las tareas son privadas. Solo las puede administrar su dueño.
* Los usuarios pueden agregar, editar, eliminar y marcar como completa/incompleta las tareas.
* El listado de tareas debe ser paginado.
* Agregar validaciones, como no aceptar tareas sin descripción, etc.
* Buscar por descripción.
* Escribir test unitarios en el primer commit.

## Cómo utilizarlo

Puedes entrar a **127.0.0.1:8000/es/swagger/** para ver información de los endpoints.

## Lanzar el proyecto

* Debes crear el archivo **.env** definiendo las variables de entorno:

```
#Django
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=
SECRET_KEY=

ALLOWED_HOSTS=
```

#### Correr el proyecto en un servidor local.

``` bash
make build
make up
make migrate
make makemessages
make compilemessages
```

#### Construye y lanza el proyecto en tu servidor de producción.

``` bash
make prod-buil
make prod-run
make prod-migrate
make prod-makemessages
make prod-compilemessages
```



