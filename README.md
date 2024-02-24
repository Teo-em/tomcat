# Tomcat

**Tomcat** es el nombre que le di a este bot de discord escrito en Python.
La idea principal es la de extenderles a mis amigos las herramientas que me brinda un entorno basado en linux mediante discord, dado que muchas de las funciones que se invocan son solo "pasamanos" a programas ejecutados en mi máquina, como yt-dlp, ffmpeg, translate-shell. Muchas de las funcionalidades fueron ideas de ellos y siempre estoy dispuesto a escuchar y tratar de implementar nuevas ideas.

## Funciones

Dentro de las funciones programadas están: descargar audios de videos de [varias plataformas](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md), mostrar el avatar de un miembro del canal, "cara o cruz" con la clásica moneda del peso argentino, recordatorio de cumpleaños, mostrar el precio del dolar blue, mensajes anónimos (se limita a personas que compartan servidor), traducir texto al español y una función que cuando se ejecuta, independientemente de lo que esté haciendo, toma una captura de pantalla y la envía.

## Uso

tom [opción]

**Opciones:**
-***-a, --audio**       Descarga el audio de un video y lo envía
-*    **--avatar**      Muestra el avatar de un usuario
-***-c, --cara-o-cruz** 50/50 cara o cruz.
-*    **--cumple**      Manejo de las fechas de cumpleaños, el bot avisa por general del servidor.
-*      **add dd/mm/aaaa** Agrega la fecha propia al recordatorio.
-*      **delete**         Elimina el recordatorio.
-***-d, --dolar**       Imprime el precio del dólar blue en pesos.
-***-h, --help**        Imprime este mensaje.
-***-m, --mensaje [usuario] [texto]** Envía un mensaje a "usuario".
-*        Usuario puede ser el username, el tag o id => <@id>
-***-q, --que-hace-teo?** Qué hace teo?(deprecated).
-***-t, --traducir [texto]** Traduce texto al español.
