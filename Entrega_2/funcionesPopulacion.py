#------------------------------ Imports----------------------------------------#
import random
import hashlib
from datetime import date, datetime
from random import randint

#-------------------------- Variables globales---------------------------------#
usernameFile = "usernames.txt"  #Archivo con 100 Usernames
paisesFile = "paises.txt"       #Archivo con 195 Nombre de paises
juegos = "juegos_clean.txt"     #Archivo procesado con datos de juegos
emailArray = ("gmail.com", "outlook.com", "sansano.usm.cl") # Emails posibles
base = 3500                     # Base para el precio de los juegos
meses = {"Jan":1 ,"Feb":2, "Mar":3, "Apr": 4, "May": 5, "Jun":6, "Jul": 7, "Aug":8, "Sep":9, "Oct": 10, "Nov":11, "Dec":12} # NombreMes a Numeros
diasMes = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}                           # Cantidad de dias por mes
dlcPorcentage = 0.8              # Porcentaje de DLC por total de juegos
maxDLC = 3                       # Numero maximo de DLC por juego
descFactor = 0.6                 # Porcentaje de items con descuento
#------------------------------ Funciones ------------------------------------#
# [Generacion Usuarios] - n : Numero de usuarios a generar, maximo 100

def generateUsers(n):
    file = open(usernameFile,encoding="utf8")
    paises = open(paisesFile,encoding="utf8").readlines()
    retorno = []
    for user in file:
        user = user.strip()
        emailsuffix = emailArray[randint(0,len(emailArray)-1)]
        email = user+"@"+emailsuffix
        pais = paises[randint(0, len(paises)-1)].strip()
        passwordHash = hashlib.md5(user.encode()).hexdigest()
        anno = 2000 + randint(0, 20)
        month = randint(1, 12)
        day = randint(1, 28)
        hour = randint(0,23)
        minutes = randint(0, 59)
        seconds = randint(0,59)
        DT = datetime(anno, month, day, hour, minutes, seconds)
        retorno.append((user, email, pais, passwordHash, DT))
        if(len(retorno) == n):
            break
    return retorno

# [Generacion Juegos] - archivo: Con informacion procesada de juegos
#                     - base : Base para el calculo del precio de juegos
#                     - meses: diccionario de nombre mes a numero
#                     - n : Numero de juegos a generar
def generateGames(archivo,base,meses,n):
    arch = open(archivo,encoding="utf8")
    retorno = []
    for linea in arch:
        juego,consola,develop,valoracion,ventas,lanzamiento,actualizacion = linea.strip().split("\t")
        precio = base*randint(1,10)
        categoria = randint(1,5)
        lanzamiento = lanzamiento.split(" ")
        lanzamiento[0] = lanzamiento[0][:2]
        lanzamiento[1] = meses[lanzamiento[1]]
        hour = randint(0,23)
        minutes = randint(0, 59)
        seconds = randint(0,59)
        day,month,year = list(map(int,lanzamiento))
        if year <= 20:
            year += 2000
        else:
            year += 1900
        DT =  datetime(year, month, day, hour, minutes, seconds)
        retorno.append((juego,develop,precio,categoria,DT))
    return retorno[:n]

# [Generacion DLC] - gameArray: Resultado de query que tiene todos los juegos
#                               listados en la tabla.
def generateDLC(gameArray):
    retorno = []
    nGames = len(gameArray)
    nDLC = round(dlcPorcentage*nGames)
    for i in range(nDLC):
        gameIndex = randint(0,len(gameArray)-1)
        nDLC_igame = randint(0, maxDLC)
        if(nDLC_igame == 0):
            continue
        else:
            gameID = gameArray[gameIndex][0]
            gameDate = gameArray[gameIndex][2]
            dates = []
            gameName = gameArray[gameIndex][1]
            for date in range(nDLC_igame):
                year = randint(gameDate.year,2020)
                month = randint(gameDate.month, 12)
                day = randint(1, diasMes[month])
                DT = datetime(year,month,day, gameDate.hour, gameDate.minute, gameDate.second)
                dates.append(DT)
            dates.sort()
            for j in range(nDLC_igame):
                name = gameName + " " + str(j+1)
                precio = base*(randint(1,5))
                retorno.append((gameID, name, dates[j], precio))
            del gameArray[gameIndex]
    return retorno

# [Generacion bundles] -info_juego: resultado query juegos en tabla
#                      -info_dlc: resultado query dlc en tabla
def generateBundles(info_juego,info_dlc):
    games = len(info_juego)
    dlcs = len(info_dlc)
    prec_juegos = {}
    prec_dlcs = {}
    id_dlcs = []
    id_games = []
    dates = []
    for id,precio,DT in info_juego:
        prec_juegos[id] = int(precio)
        id_games.append(id)
        dates.append(DT)
    for id,precio,DT in info_dlc:
        prec_dlcs[id] = int(precio)
        id_dlcs.append(id)
        dates.append(DT)
    cant_bundles = games//5 # Hay n°Juegos /5 bundles
    bundles = []
    for i in range(cant_bundles):
        type1 = 0
        if len(id_games) != 0:
            id1 = random.choice(id_games)
            del id_games[id_games.index(id1)]
            precio1 = prec_juegos[id1]
        else:
            id1 = None
        type2 = randint(0,1)
        if type2:
            if len(id_dlcs) != 0:
                id2 = random.choice(id_dlcs)
                del id_dlcs[id_dlcs.index(id2)]
                precio2 = prec_dlcs[id2]
            else:
                id2 = None
        else:
            if len(id_games) != 0:
                id2 = random.choice(id_games)
                del id_games[id_games.index(id2)]
                precio2 = prec_juegos[id2]
            else:
                id2 = None
        type3 = randint(0,2)
        if type3 == 1:
            if len(id_dlcs) != 0:
                id3 = random.choice(id_dlcs)
                del id_dlcs[id_dlcs.index(id3)]
                precio3 = prec_dlcs[id3]
            else:
                id3 = None
        elif type3 == 0:
            if len(id_games) != 0:
                id3 = random.choice(id_games)
                del id_games[id_games.index(id3)]
                precio3 = prec_juegos[id3]
            else:
                id3 = None
        else:
            id3 = None
            precio3 = 0
        dcto = randint(50,90)/100
        dates.sort()
        proxDate = dates[-1]
        DT = generateDT(proxDate, proxDate.year)
        bundles.append((type1,id1,round(precio1*dcto),
                        type2,id2,round(precio2*dcto),
                        type3, id3,round(precio3*dcto),
                        round((precio1 + precio2 + precio3)*dcto), DT))
    return bundles

def unpackResult(result, idPos):
    retorno = {}
    for i in result:
        id = i[idPos]
        tempVals = []
        for j in i:
            if(id != j):
                tempVals.append(j)
        retorno[id] = tempVals
    return retorno

def generateDescuentos(items, juegos, dlcs, bundles):
    # items  = (idItem, idType, idJuego, idDLC, idBundle)
    # juegos = (idJuego, fechaRelease)
    # dlc    = (idDLC, fechaRelease)
    # bundle = (idBundle, fechaRelease)
    retorno = []
    lowerDesc = 15
    upperDesc = 75
    tempItems = items
    gamesUnpacked  = unpackResult(juegos, 0)
    dlcUnpacked    = unpackResult(dlcs, 0)
    bundleUnpacked = unpackResult(bundles, 0)
    unpacks = {0:gamesUnpacked, 1:dlcUnpacked, 2:bundleUnpacked}
    cantDescuentos = round(len(items)*descFactor)
    for i in range(cantDescuentos):
        if(len(tempItems) == 0):
            break
        tempID = randint(0, len(tempItems)-1)
        porcentaje = randint(lowerDesc, upperDesc)
        itemID = tempItems[tempID][0]
        itemType = tempItems[tempID][1]
        if(itemType == 0):
            idMap = tempItems[tempID][2]
        elif(itemType == 1):
            idMap = tempItems[tempID][3]
        else:
            idMap = tempItems[tempID][4]
        fromDT = generateDT(unpacks[itemType][idMap][0], 2020)
        untilDT= generateDT(fromDT, 2020)
        tuple = (itemID, porcentaje, fromDT, untilDT)
        retorno.append(tuple)
        del tempItems[tempID]
    return retorno

def generar_licencia():
    S = "ABCDEFGHIJKLMNOPQRSTVWXYZ"
    licencia = ""
    for i in range(4):
        for i in range(4):
            caract = random.choice(S)
            licencia += caract
        licencia += "-"

    return licencia[:-1]

def horas_instal(fecha):
    instalado = random.randint(0,1)
    if instalado:
        anno,mes,dia = list(map(int,str(datetime.now()).split(" ")[0].split("-")))
        days_now = anno*365 + mes*30 + dia
        aaaa,mm,dd = list(map(int,str(fecha).split(" ")[0].split("-")))
        days = aaaa*365 +mm*30+ dd
        hrs =  abs(round((days_now - days)*2/24))
    else:
        hrs = 0
    return [hrs,instalado]


def item2Bundles(items):
    retorno = {}
    for item in items:
        idType = item[1]
        if(idType != 2):
            continue
        idItem = item[0]
        retorno[idItem] = item[idType + 2]
    return retorno

def generateBiblioteca(recibos, items, bundles):
    retorno = []
    mappedItems = item2Bundles(items)
    itemsUnpacked = unpackItems(items)
    bundlesUnpacked = unpackBundles(bundles)
    for recibo in recibos:
        idRecibo = recibo[0]
        idUsuario = recibo[1]
        idItem = recibo[2]
        DT = recibo[3]
        if(idItem in mappedItems.keys()):
            #Juegos
            bundleID = mappedItems[idItem]
            for element in bundlesUnpacked[bundleID][0]:
                elementID = itemsUnpacked[0][element]
                licencia = generar_licencia()
                hrs,instalado = horas_instal(DT)
                tupla = (idUsuario, idRecibo, elementID, licencia, hrs, instalado, DT)
                retorno.append(tupla)
            #DLC
            for element in bundlesUnpacked[bundleID][1]:
                elementID = itemsUnpacked[1][element]
                licencia = generar_licencia()
                hrs,instalado = horas_instal(DT)
                tupla = (idUsuario, idRecibo, elementID, licencia, hrs, instalado, DT)
                retorno.append(tupla)
        else:
            licencia = generar_licencia()
            hrs,instalado = horas_instal(DT)
            tupla = (idUsuario, idRecibo, idItem, licencia, hrs, instalado, DT)
            retorno.append(tupla)
    return retorno

def unpackDescuentos(descuentos, items):
    # descuento -> (idDescuento, idItem, porcentaje, fechaInicio, fechaTermino)
    # items     -> (idItem, idType, idJuego, idDLC, idbundle)
    descJuego = {}
    descDLC = {}
    descBundle = {}
    retorno = {0:descJuego, 1:descDLC, 2:descBundle}
    for item in items:
        idItem = item[0]
        idType = item[1]
        idMap = item[2 + idType]
        for descuento in descuentos:
            idDesc = descuento[0]
            itemDesc = descuento[1]
            if(idItem == itemDesc):
                porcentaje = descuento[2]
                fechaInicio = descuento[3]
                fechaTermino = descuento[4]
                retorno[idType][idMap] = (idDesc, porcentaje, fechaInicio, fechaTermino)
    return retorno

def chargeItem(idUsuario, idType, idItem, costo, descUnpacked, retList, lowerDate, itemsUnpacked):
    #Generacion fechaCompra
    DT = generateDT(lowerDate,2018)
    if(idItem in descUnpacked[idType].keys()) and (descUnpacked[idType][idItem][3] >= DT) and (descUnpacked[idType][idItem][2] <= DT):
        #Tiene descuento aplicable a la fecha de compra
        desc = descUnpacked[idType][idItem][1]
        idDescuento = descUnpacked[idType][idItem][0]

    else:
        desc = 0
        idDescuento = None
    desc = desc /100
    ValorPagado = (1-desc)*costo
    idMap = itemsUnpacked[idType][idItem]
    tuple = (idUsuario, idMap, idDescuento, costo, ValorPagado, DT)
    retList.append(tuple)

def generateDT(lowerDate, lowerYear):
    year = randint(lowerYear,2020)
    if(lowerDate == None):
        month = randint(1,12)
        day = randint(1, diasMes[month])
    elif(lowerDate.year == 2020):
        month = randint(lowerDate.month, 12)
        day = randint(1, diasMes[month])
    else:
        month = randint(1,12)
        day = randint(1, diasMes[month])
    hour = randint(0,23)
    minute = randint(0,59)
    second = randint(0,59)
    if(month == 9) and (day == 6) and (hour == 0):
        hour += 1
    DT  = datetime(year, month, day, hour, minute, second)
    return DT

def unpackBundles(bundles):
    retorno = {}
    for bundle in bundles:
        games = []
        dlc = []
        bundleID = bundle[0]
        for i in range(3):
            index = 1 + (3*i)
            if(bundle[index] == 0):
                games.append(bundle[index + 1])
            elif(bundle[index] == 1):
                dlc.append(bundle[index + 1])
        retorno[bundleID] = {0:games, 1:dlc}
    return retorno

def listIntersection(listA, listB):
    flag = False
    for i in listA:
        if(i in listB):
            flag = True
            break
    return flag

def lowestDate(dates):
    lowest = dates[0]
    for date in dates:
        if(lowest > date):
            lowest = date
    return lowest

def unpackDLC(dlcs):
    retorno = {}
    for dlc in dlcs:
        idGame = dlc[1]
        idDLC = dlc[0]
        if (idGame in retorno.keys()):
            retorno[idGame] += [idDLC]
        else:
            retorno[idGame] = [idDLC]
    return retorno

def unpackItems(items):
    juegos = {}
    dlc = {}
    bundles = {}
    retorno = {0:juegos, 1:dlc, 2:bundles}
    for item in items:
        itemType = item[1]
        idItem = item[0]
        idMap = item[itemType + 2]
        retorno[itemType][idMap] = idItem
    return retorno

def generateRecibos(usuarios, juegos, bundles, dlcs, descuentos, items):
    retorno = []
    juegosPerUser = {}
    dlcPerUser = {}
    # items   -> (idItem, idType, idA, idB, idC)
    # Usuario -> (idUser, fechaRegistro)
    # Juegos  -> (idJuego, costo)
    # Bundles -> (idBundle, idTypeA, idA, idTypeB, idB, idTypeC, idC, costo, DT)
    # desc_new -> (idDescuento, idItem, porcentaje, fechaInicio, fechaTermino)
    # desc_old    -> (idDescuento, porcentaje, fechaTermino, idType, idAplicado, fechaInicio)
    # dlc     -> (idDLC, idJuego, releaseDate, precio)
    itemsUnpacked= unpackItems(items)
    descUnpacked = unpackDescuentos(descuentos,items)
    bundUnpacked = unpackBundles(bundles)
    dlcsUnpacked = unpackDLC(dlcs)
    for user in usuarios:
        idUser = user[0]
        lowerDate = user[1]
        nCompras = randint(0, len(juegos))
        tempGames = juegos.copy()
        tempBundles = bundles.copy()
        tempDLCS = dlcs.copy()
        juegosPerUser[idUser] = []
        dlcPerUser[idUser] = []
        # Generar recibo juegos
        for i in range(nCompras):
            if(len(tempGames) == 0):
                #No hay mas juegos que agregar
                break
            tempID = randint(0, len(tempGames)-1)
            idJuego = tempGames[tempID][0]
            costo = tempGames[tempID][1]
            chargeItem(idUser, 0, idJuego, costo, descUnpacked, retorno, lowerDate, itemsUnpacked)
            juegosPerUser[idUser] += [idJuego]
            del tempGames[tempID]
        # Generar recibo bundles
        nCompras = randint(0, len(bundles))
        for j in range(nCompras):
            if(len(tempBundles) == 0):
                #No hay mas bundles que agregar
                break
            tempID = randint(0, len(tempBundles)-1)
            idBundle = tempBundles[tempID][0]
            gamesInBundle = bundUnpacked[idBundle][0]
            dlcsInBundle = bundUnpacked[idBundle][1]
            if(listIntersection(gamesInBundle, juegosPerUser[idUser])):
                del tempBundles[tempID]
                continue
            else:
                costo = tempBundles[tempID][7]
                lowerDate_2 = tempBundles[tempID][8]
                chargeItem(idUser, 2, idBundle, costo, descUnpacked, retorno, lowestDate([lowerDate, lowerDate_2]), itemsUnpacked)
                juegosPerUser[idUser] += gamesInBundle
                dlcPerUser[idUser] += dlcsInBundle
                del tempBundles[tempID]

        # Generar recibo DLC
        nCompras = randint(0, len(dlcs))
        for k in range(nCompras):
            if(len(tempDLCS) == 0):
                #No hay mas DLCs que agregas
                break
            tempID = randint(0, len(tempDLCS)-1)
            idDLC = tempDLCS[tempID][0]
            idJuego = tempDLCS[tempID][1]
            if(idUser in dlcPerUser.keys()) and ((idDLC in dlcPerUser[idUser]) or (idJuego not in dlcsUnpacked.keys())):
                del tempDLCS[tempID]
                continue
            else:
                costo = tempDLCS[tempID][3]
                lowerDate_3 = tempDLCS[tempID][2]
                chargeItem(idUser, 1, idDLC, costo, descUnpacked, retorno, lowestDate([lowerDate, lowerDate_3]), itemsUnpacked)
                dlcPerUser[idUser] += [idDLC]
                del tempDLCS[tempID]
    retorno.sort()
    return retorno

def generateItems(juegos, dlcs, bundles):
    retorno = []
    # Se ingresan juegos
    idType = 0
    for juego in juegos:
        tupla = (idType, juego[0], None, None)
        retorno.append(tupla)
    # Se ingresan dlcs
    idType = 1
    for dlc in dlcs:
        tupla = (idType, None, dlc[0], None)
        retorno.append(tupla)
    # Se ingresan bundles
    idType = 2
    for bundle in bundles:
        tupla = (idType, None, None, bundle[0])
        retorno.append(tupla)
    return retorno
