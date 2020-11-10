# -*- coding: utf-8 -*-

import datetime

def toFixed(numObj, digits = 0):
    return f'{numObj:.{digits}f}'

def currencySymbol(code):
    return {
        'USD': '$',
        'EUR': '€',
        'RUB': '₽',
        'BTC': '฿',
        'mBTC': 'm฿',
    }[code]

def currencyStep(code):
    return {
        'USD': '0.01',
        'EUR': '0.01',
        'RUB': '0.01',
        'BTC': 'any',
        'mBTC': 'any',
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
    
def categoryIcon(identifier):
    return {
        'unspecified': '❓',
        'notrack': '❔',
        'charity': '🎗',
        'household': '🛀', 
        'lodging': '🏠', 
        'books': '📚', 
        'music': '🎵', 
        'culture': '🎭', 
        'catering': '🍔', 
        'clothes': '👔', 
        'cosmetics': '💄', 
        'gifts': '🎁', 
        'food': '🍏', 
        'meds': '💊', 
        'communication': '📱', 
        'software': '🎮', 
        'tech': '💻', 
        'transport': '🚗', 
        'hobby': '🎨',
        'salary': '💼',
        'fee': '💲',
        'find': '💲',
        'ecommerce': '💰',
        'crowdfunding': '💖',
        'interest': '💵',
        'trading': '📈',
        'art': '🖼',
        'other': '❓'
    }[identifier]
    
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
        'cosmetics': '💄 Косметика', 
        'gifts': '🎁 Подарки', 
        'food': '🍏 Продукты питания', 
        'meds': '💊 Лекарства', 
        'communication': '📱 Связь', 
        'software': '🎮 Софт, игры', 
        'tech': '💻 Техника', 
        'transport': '🚗 Транспорт', 
        'hobby': '🎨 Хобби и творчество',
        'salary': '💼 Зарплата',
        'fee': '💲 Гонорары',
        'find': '💲 Находка',
        'ecommerce': '💰 Э-коммерция и фриланс',
        'crowdfunding': '💖 Краудфандинг',
        'interest': '💵 Проценты от банков',
        'trading': '📈 Трейдинг',
        'art': '🖼️ Продажа картин',
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

def currentDateTime():
    return datetime.datetime.now()