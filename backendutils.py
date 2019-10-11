# -*- coding: utf-8 -*-

import datetime

def toFixed(numObj, digits = 0):
    return f'{numObj:.{digits}f}'

def currencySymbol(code):
    return {
        'USD': '$',
        'EUR': '€',
        'RUB': '₽'
    }[code]

def money(value, currencyCode):
    curr = currencySymbol(currencyCode)
    return '{:,.2f}'.format(value).replace(',', ' ').replace('.', ',') + ' ' + curr

def transactionAmount(value, currencyCode):
    curr = currencySymbol(currencyCode)
    sign = ''
    if value > 0:
        sign = '+'
    return sign + '{:,.2f}'.format(value).replace(',', ' ').replace('.', ',') + ' ' + curr

def datetimeFromStr(dts):
    return datetime.datetime.strptime(dts, '%Y-%m-%d %H:%M:%S')
    
def category(identifier):
    return {
        'unspecified': '❓ [Не указано]',
        'notrack': '❔ [Вне отчетности]',
        'charity': '🎗 Благотворительность',
        'household': '🛀 Бытовые товары', 
        'lodging': '🏠 Жилье', 
        'books': '📚 Книги', 
        'music': '🎵 Музыка', 
        'culture': '🎭 Культурный досуг', 
        'catering': '🍔 Общепит', 
        'clothes': '👔 Одежда', 
        'gifts': '🎁 Подарки', 
        'food': '🍏 Продукты питания', 
        'communication': '📱 Связь', 
        'software': '🎮 Софт, игры', 
        'tech': '💻 Техника', 
        'transport': '🚗 Транспорт', 
        'hobby': '🎨 Хобби и творчество',
        'salary': '💼 Зарплата',
        'ecommerce': '💰 Э-коммерция',
        'crowdfunding': '💖 Краудфандинг',
        'interest': '💵 Проценты от банков',
        'other': '❓ Прочее'
    }[identifier]
    
def month(num):
    return [
        'январь',
        'февраль',
        'март',
        'апрель',
        'май',
        'июнь',
        'июль',
        'август',
        'сентябрь',
        'октябрь',
        'ноябрь',
        'декабрь'
    ][num]