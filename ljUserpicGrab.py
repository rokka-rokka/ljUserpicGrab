#!/usr/bin/python
# -*- coding: utf-8 -*-

#------------------------------#
#       ljUserpicGrab.py       #
#          Version 0.5         #
#                              #
#   Copyright (c) 2006-2017    #
#------------------------------#

#-- v0.5 (12/2017)
#-- обновление регулярных выражений в связи с переходом на https


import re, urllib, os

# =========/ Настройка скрипта ========= #

nUsers = 20           # Количество юзеров для граббинга
upDir = 'userpics'    # Папка для файлов
# ========= Настройка скрипта /========= #


# ----------/ Функция получения случайного ника жж-юзера ---------

ljUnFilter = r'https://[\w-]+\.livejournal.com/data/rss'
reLjUnFilter = re.compile(ljUnFilter)

def getRandomLJUser():
    while True:
        try:
            page = urllib.urlopen('https://www.livejournal.com/random.bml').read()
        except:
            continue
        list = []
        list.extend(reLjUnFilter.findall(page))
        print list[0][8:-24][:-1]
        return list[0][8:-24][:-1]
    
# ---------- Функция получения случайного ника жж-юзера /---------


# Ссылка на страницу с юзерпиками юзера
userpicUrl = 'https://www.livejournal.com/allpics.bml?user='
# RE-строка фильтра для ссылок на юзерпики
filter = r'https://l-userpic.livejournal.com/[\d]+/[\d]+'
reFilter = re.compile(filter)

print 'ljUserpicGrab.py ver. 0.4'

# Проверяем существование папки
if os.access(upDir,os.F_OK) == False:
    os.mkdir(upDir) # Создаём папку для юзерпиков

nVUsers = 0 # Cчётчик юзеров
while nVUsers != nUsers:
    upUrlsList = [] # Список со ссылками на юзерпики юзера
    # Получаем случаное имя юзера
    ljUserName = getRandomLJUser()
    # Получаем страницу с юзерпиками
    upPage = urllib.urlopen(userpicUrl + ljUserName)
    # Получаем все ссылки со страницы
    upUrlsList.extend(reFilter.findall(upPage.read()))
    # Проверяем, есть ли юзерпики у юзера
    if len(upUrlsList) != 0:
        print '>> ljUser \'%s\' (%s of %s): %s userpics' % (
            ljUserName, nVUsers+1, nUsers, len(upUrlsList))
        # Проверяем существование папки
        if os.access(upDir+'/'+ljUserName+'/',os.F_OK) == False:
            # Создаём папку для юзерпиков с именем юзера
            os.makedirs(upDir+'/'+ljUserName+'/')
        else: # Папка существует - значит, юзерпики уже скачивали
            continue # Смотрим следующего юзера
    else: # Нет - смотрим следующего юзера
        continue

    nUserpic = 0 # Число юзерпиков (счётчик)
    for upUrl in upUrlsList:
        # Открываем ссылку на файл юзерпика
        upFile = urllib.urlopen(upUrl)
        # Определяем тип файла юзерпика (ЖЖ не даёт расширения файлов)
        typeFile = upFile.info()['content-type']
        if   typeFile == 'image/gif' : fileTypeExt = 'gif'
        elif typeFile == 'image/jpeg': fileTypeExt = 'jpg'
        elif typeFile == 'image/png' : fileTypeExt = 'png'
        else:
            print 'Unknown content type', typeFile # Неизвестный файл
            continue # Смотрим следующую ссылку
    
        upPathFile = '%s/%s/%s.%s' % (upDir,ljUserName,nUserpic+1,fileTypeExt)
        
        print 'Saving %s...' % upPathFile,
        
        # Сохраняем полученный файл юзерпика
        upOutputFile = open(upPathFile, 'wb')
        upOutputFile.write(upFile.read())
        print 'Ok'
        # Закрываем файловые потоки
        upOutputFile.close()
        upFile.close()
        nUserpic += 1 # Увеличивыем число юзерпиков

    nVUsers += 1 # Увеличиваем число юзеров

print 'Done'