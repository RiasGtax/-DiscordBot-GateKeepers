# Bot creado por RiasGtax

# Imports
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
from datetime import datetime, timedelta
import requests
import json

bot = commands.Bot(command_prefix="!")
canalesActivos = []
listaCanal = ["se1", "se2", "se3", "se4", "se5", "se6",
                "ba1", "ba2", "ba3", "ba4", "ba5", "ba6",
                "va1", "va2", "va3", "va4", "va5", "va6",
                "ca1", "ca2", "ca3", "ca4", "ca5", "ca6",
                "ve1", "ve2", "ve3", "ve4", "ve5", "ve6",
                "me1", "me2", "me3", "me4", "me5", "me6",
                "ka1", "ka2", "ka3", "ka4"]
canalDestino = "general"   # NOTA: ESTE ES EL NOMBRE DEL CANAL EN EL CUAL SOLO LEERA EL BOT,
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

        if not canalesActivos:
            await crearEmbed("Lista vacia", "No hay ningun canal en la lista, prueba añadiendo uno antes!", 0x4ac1db) 

        for canal in canalesActivos:
            diccionario = requests.get('http://elastic:123456@localhost:9200/' + canal + "/estado/_search")
            diccionarioParsed = json.loads(diccionario.content)
            if diccionarioParsed['hits']['hits'][0]['_source'][canal]['tipo'] == 2:
                await crearEmbed(diccionarioParsed['hits']['hits'][0]['_index'].upper(), "Estado: {0} - Hora: {1}".format(diccionarioParsed['hits']['hits'][0]['_source'][canal]['estado'].upper(), diccionarioParsed['hits']['hits'][0]['_source'][canal]['hora']), 0x5bba4c)
            else:
                await crearEmbed(diccionarioParsed['hits']['hits'][0]['_index'].upper(), "Estado: {0} - Hora: {1} - Ventana: {2} / {3} | En Desierto: {4} / {5}".format(diccionarioParsed['hits']['hits'][0]['_source'][canal]['estado'].upper(), diccionarioParsed['hits']['hits'][0]['_source'][canal]['hora'], diccionarioParsed['hits']['hits'][0]['_source'][canal]['ventana1'], diccionarioParsed['hits']['hits'][0]['_source'][canal]['ventana2'], diccionarioParsed['hits']['hits'][0]['_source'][canal]['desierto1'], diccionarioParsed['hits']['hits'][0]['_source'][canal]['desierto2']), 0x5bba4c)


#   Añadir canales
@bot.command(pass_context=True)
async def vivo(ctx, canal, *args):
    if str(ctx.message.channel) == canalDestino:
        async for mensaje in bot.logs_from(ctx.message.channel, limit=15):
            await bot.delete_message(mensaje)
            await asyncio.sleep(1)

        if canal.lower() in listaCanal:
            if canal.lower() not in canalesActivos:
                dtActual = datetime.now()
                mapa = {canal.lower() : {"tipo" : 2, "estado" : "vivo", "hora" : dtActual.strftime("%H:%M")}}
                requests.post('http://elastic:123456@localhost:9200/' + canal.lower() + "/estado", data=json.dumps(mapa), headers={"Content-type" : "application/json"})
                canalesActivos.append(canal.lower())
                await crearEmbed("GateKeeper Añadido", "GateKeeper añadido al canal {0}".format(canal.upper()), 0x5bba4c)
            else:
                requests.delete('http://elastic:123456@localhost:9200/' + canal)
                dtActual = datetime.now()
                mapa = {canal.lower() : {"tipo" : 2, "estado" : "vivo", "hora" : dtActual.strftime("%H:%M")}}
                requests.post('http://elastic:123456@localhost:9200/' + canal.lower() + "/estado", data=json.dumps(mapa), headers={"Content-type" : "application/json"})
                await crearEmbed("GateKeeper Añadido", "GateKeeper añadido al canal {0}".format(canal.upper()), 0x5bba4c)
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
            if canal.lower() not in canalesActivos:
                mapa = {canal.lower() : {"tipo" : 4, "estado" : "muerto", "hora" : dtActual.strftime("%H:%M"), "ventana1" : dtMin.strftime("%H:%M"), "ventana2" : dtMax.strftime("%H:%M"), "desierto1" : dtDMin.strftime("%H:%M"), "desierto2" : dtDMax.strftime("%H:%M")}}
                requests.post('http://elastic:123456@localhost:9200/' + canal.lower() + "/estado", data=json.dumps(mapa), headers={"Content-type" : "application/json"})
                canalesActivos.append(canal.lower())
                await crearEmbed("GateKeeper Añadido", "GateKeeper añadido al canal {0}".format(canal.upper()), 0x5bba4c)
            else:
                requests.delete('http://elastic:123456@localhost:9200/' + canal)
                mapa = {canal.lower() : {"tipo" : 4, "estado" : "muerto", "hora" : dtActual.strftime("%H:%M"), "ventana1" : dtMin.strftime("%H:%M"), "ventana2" : dtMax.strftime("%H:%M"), "desierto1" : dtDMin.strftime("%H:%M"), "desierto2" : dtDMax.strftime("%H:%M")}}
                requests.post('http://elastic:123456@localhost:9200/' + canal.lower() + "/estado", data=json.dumps(mapa), headers={"Content-type" : "application/json"})
                await crearEmbed("GateKeeper Añadido", "GateKeeper añadido al canal {0}".format(canal.upper()), 0x5bba4c)
        else:
            await crearEmbed("ERROR", "No has seleccionado un canal o estado disponible, revisa !info para mas informacion", 0xdb4a4a)


#   Borrar canal
@bot.command(pass_context=True)
async def borrar(ctx, canal, *args):
    if str(ctx.message.channel) == canalDestino:
        async for mensaje in bot.logs_from(ctx.message.channel, limit=15):
            await bot.delete_message(mensaje)
            await asyncio.sleep(1)

        if canal in canalesActivos:
            requests.delete('http://elastic:123456@localhost:9200/' + canal)
            canalesActivos.remove(canal)
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

        for entrada in canalesActivos:
            requests.delete('http://elastic:123456@localhost:9200/' + entrada)
            
        canalesActivos.clear()
        await crearEmbed("Lista limpiada", "Se ha limpiado correctamente el listado de canales", 0x5bba4c)

bot.run("TOKEN AQUI!")
