# Bot creado por RiasGtax

# Imports
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from datetime import datetime, timedelta

bot = commands.Bot(command_prefix="!")
diccionario = {}
listaCanal = ["se1", "se2", "se3", "se4", "se5", "se6",
                "ba1", "ba2", "ba3", "ba4", "ba5", "ba6",
                "va1", "va2", "va3", "va4", "va5", "va6",
                "ca1", "ca2", "ca3", "ca4", "ca5", "ca6",
                "ve1", "ve2", "ve3", "ve4", "ve5", "ve6",
                "me1", "me2", "me3", "me4", "me5", "me6",
                "ka1", "ka2", "ka3", "ka4"]
canalDestino = "gatekeepers"   # NOTA: ESTE ES EL NOMBRE DEL CANAL EN EL CUAL SOLO LEERA EL BOT,
# SI CAMBIAIS EL NOMBRE DE CANAL TAMBIEN CAMBIADLO AQUI!! CAMBIAD SOLO LO QUE ESTA DENTRO DE LAS ".


# Metodos
#   Ready
@bot.event
async def on_ready():
    print ("Bot en el servidor")


#   Crear Embed
async def crearEmbed(nombre, valor, color):
    embed = discord.Embed(title="---- INFO ----", color=color)
    embed.set_footer(text="GateKeepers Bot")
    embed.add_field(name=nombre, value=valor)
    await bot.say(embed=embed)


#   Info
@bot.command(pass_context=True)
async def info(ctx):
    if str(ctx.message.channel) == canalDestino:
        async for mensaje in bot.logs_from(ctx.message.channel, limit=15):
            await bot.delete_message(mensaje)
            await asyncio.sleep(1)

        await crearEmbed("Comandos disponibles: ", "!info - !lista - !vivo (canal) - !muerto (canal) - !borrar (canal) - !limpiar", 0x4ac1db)
        await crearEmbed("Formato de los canales: ", "Los canales DEBEN insertarse abreviados, Ejemplo: Mediah4 -> me4", 0x4ac1db)


#    Consultar estado
@bot.command(pass_context=True)
async def lista(ctx):
    if str(ctx.message.channel) == canalDestino:
        async for mensaje in bot.logs_from(ctx.message.channel, limit=15):
            await bot.delete_message(mensaje)
            await asyncio.sleep(1)

        embed = discord.Embed(title="---- INFO ----", color=0xa76df2)
        embed.set_footer(text="GateKeepers Bot")
        for canal in diccionario.keys():
            if len(diccionario.get(canal)) == 2:
                embed.add_field(name=canal.upper(), value="Estado: {0} - Hora: {1}".format(diccionario.get(canal)[0].upper(), diccionario.get(canal)[1]))
            else:
                embed.add_field(name=canal.upper(), value="Estado: {0} - Hora: {1} - Ventana: {2} / {3} | En Desierto: {4} / {5}".format(diccionario.get(canal)[0].upper(), diccionario.get(canal)[1], diccionario.get(canal)[2], diccionario.get(canal)[3], diccionario.get(canal)[4], diccionario.get(canal)[5]))

        await bot.say(embed=embed)


#   Añadir canales
@bot.command(pass_context=True)
async def vivo(ctx, canal, *args):
    if str(ctx.message.channel) == canalDestino:
        async for mensaje in bot.logs_from(ctx.message.channel, limit=15):
            await bot.delete_message(mensaje)
            await asyncio.sleep(1)

        if canal.lower() in listaCanal:
            await crearEmbed("GateKeeper Añadido", "GateKeeper añadido al canal {0}".format(canal.upper()), 0x5bba4c)
            dtActual = datetime.now()
            diccionario[canal.lower()] = ["vivo", dtActual.strftime("%H:%M")]
        else:
            await crearEmbed("ERROR", "No has seleccionado un canal o estado disponible, revisa !info para mas informacion", 0xdb4a4a)


@bot.command(pass_context=True)
async def muerto(ctx, canal, *args):
    if str(ctx.message.channel) == canalDestino:
        async for mensaje in bot.logs_from(ctx.message.channel, limit=15):
            await bot.delete_message(mensaje)
            await asyncio.sleep(1)

        if canal in listaCanal:
            dtActual = datetime.now()
            dtMin = dtActual + timedelta(hours=6)
            dtMax = dtActual + timedelta(hours=8)
            dtDMin = dtActual + timedelta(hours=8)
            dtDMax = dtActual + timedelta(hours=12)
            diccionario[canal.lower()] = ["muerto", dtActual.strftime("%H:%M"), dtMin.strftime("%H:%M"), dtMax.strftime("%H:%M"), dtDMin.strftime("%H:%M"), dtDMax.strftime("%H:%M")]
            await crearEmbed("GateKeeper Añadido", "GateKeeper actualizado en el canal {0}".format(canal.upper()), 0x5bba4c)
        else:
            await crearEmbed("ERROR", "No has seleccionado un canal o estado disponible, revisa !info para mas informacion", 0xdb4a4a)


#   Borrar canal
@bot.command(pass_context=True)
async def borrar(ctx, canal, *args):
    if str(ctx.message.channel) == canalDestino:
        async for mensaje in bot.logs_from(ctx.message.channel, limit=15):
            await bot.delete_message(mensaje)
            await asyncio.sleep(1)

        if canal in diccionario.keys():
            diccionario.pop(canal, None)
            await crearEmbed("Canal: ", "Canal borrado correctamente", 0x5bba4c)
        else:
            await crearEmbed("ERROR", "No has seleccionado un canal de la lista, escribe !lista para ver los canales disponibles", 0xdb4a4a)


#   Limpiar estado
@bot.command(pass_context=True)
async def limpiar(ctx):
    if str(ctx.message.channel) == canalDestino:
        async for mensaje in bot.logs_from(ctx.message.channel, limit=15):
            await bot.delete_message(mensaje)
            await asyncio.sleep(1)

        diccionario.clear()
        await crearEmbed("Lista limpiada", "Se ha limpiado correctamente el listado de canales", 0x5bba4c)

bot.run("Token AQUI!")
