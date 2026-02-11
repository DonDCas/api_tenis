# Backend Tenis

## Francisco Javier Rueda Serrano 

**Index**

[TOCM]

[TOC]


# 0. Introucción

Bienvenido a mi proyecto final para el modulo de Programación de Servicios y Procesos (PSP).
Antes de empezar a explicar como trabajar con este backend quiero explicar que la elección de la tematica viene precedida de ejercicios anteriores de otros modulos que al no haber terminado de forma satisfactoria los he querido expandir un poco por gusto personal y de paso aprovechar para hacer un proyecto más grande.

En este Backend se puede trabajar con una base de datos de jugadores de tenis y competiciones y partidos. La idea es que los usuarios puedan crear y modificar partidos o añadir y modificar jugadores siempre y cuando esten registrados en la base de datos ya sea como admin o como usuarios registrados (arbitros).

La base de datos esta alojada en Postgre y la api esta configurada en base a DJango Rest con lo cual si quieres hacer uso de esta api habra que configurarlos previamente

# 1. Requisitos Previos

Pasemos a la configuración previa del host que alojará nuestro backend.

>[!IMPORTANT]
>Todo lo que se explicará a continuación sobre la instalación esta dirigido a Windows. Si buscar utilizar Linux o MAC deberás amoldar las instalaciones a tu sistema operativo.

## 🐍 Python

>[!NOTE]
>La versión utilizada de Python es (3.14.3) si se usa una anterior o posterior podria dar lugar a errores.

Empezaremos accediendo a la pagina web de python para descargarnos Python Manager a traves del siguiente link [Click aquí](https://www.python.org/downloads "Click aquí")
Una vez descargado iniciamos la instalación marcando la casilla de "**Add Python to Path**"

## 🐈‍⬛ Git

Si vas a querer acceder a este backend desde su repositorio vas a necesitar descargar e instalar como minimo Git a traves de este enlace [Click aqui](https://git-scm.com/install/windows)

## 📯Postman

Vamos a necesitar Postman para hacer pruebas una vez nuestro servidor este en funcionamiento.  Podemos descargarlo si [hacemos click aqui(https://www.postman.com/downloads/)]
