function strToRGB(str) {
    var hash = 0;
    if (str.length === 0) return hash;
    for (var i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
        hash = hash & hash;
    }
    var rgb = [0, 0, 0];
    for (var i = 0; i < 3; i++) {
        var value = (hash >> (i * 8)) & 255;
        rgb[i] = value;
    }
    return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
}

function loadJSON(url, callback) {
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState == 4 && req.status == "200") {
            callback(req.responseText);
        }
    };
    req.open("GET", url);
    req.send();
}

function currencySymbol(code) {
    return {
        USD: "$",
        EUR: "€",
        RUB: "₽"
    }[code];
}

function money(value, currencyCode) {
    var curr = currencySymbol(currencyCode);
    var v = value.toFixed(2);
    return v.replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1 ').replace(".", ",") + ' ' + curr
}

function category(identifier) {
    return {
        'unspecified': '[Не указано]',
        'notrack': '[Вне отчетности]',
        'charity': 'Благотворительность',
        'household': 'Бытовые товары', 
        'lodging': 'Жилье', 
        'books': 'Книги', 
        'music': 'Музыка', 
        'culture': 'Культурный досуг', 
        'catering': 'Общепит', 
        'clothes': 'Одежда', 
        'cosmetics': 'Косметика', 
        'gifts': 'Подарки', 
        'food': 'Продукты питания',
        'meds': 'Лекарства', 
        'communication': 'Связь', 
        'software': 'Софт, игры', 
        'tech': 'Техника', 
        'transport': 'Транспорт', 
        'hobby': 'Хобби и творчество',
        'salary': 'Зарплата',
        'fee': 'Гонорар',
        'find': 'Находка',
        'ecommerce': 'Э-коммерция',
        'crowdfunding': 'Краудфандинг',
        'interest': 'Проценты от банков',
        'other': 'Прочее'
    }[identifier];
}
