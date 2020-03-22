import "package:flutter/material.dart";
import "package:flutter/services.dart";
import "package:dropdown_formfield/dropdown_formfield.dart";
import "package:flutter_datetime_picker/flutter_datetime_picker.dart";
import "./database.dart";
import "./account.dart";
import "./transaction.dart";

class WalletAddTransaction extends StatefulWidget
{
    final WalletAccount account;
    WalletAddTransaction({Key key, this.account}): super(key: key);
    @override WalletAddTransactionState createState() => WalletAddTransactionState();
}

class WalletAddTransactionState extends State<WalletAddTransaction>
{
    final _formKey = GlobalKey<FormState>();
    String _description = "";
    String _category = "";
    double _value = 0.0;
    DateTime datetime = null;
    
    final _categories = [
        { "value": "notrack", "display": "❔ [Вне отчетности]",},
        { "value": "charity", "display": "🎗 Благотворительность", },
        { "value": "household", "display": "🛀 Бытовые товары", },
        { "value": "lodging", "display": "🏠 Жилье", },
        { "value": "books", "display": "📚 Книги", },
        { "value": "music", "display": "🎵 Музыка", },
        { "value": "culture", "display": "🎭 Культурный досуг", },
        { "value": "catering", "display": "🍔 Общепит", },
        { "value": "clothes", "display": "👔 Одежда", },
        { "value": "cosmetics", "display": "💄 Косметика", },
        { "value": "gifts", "display": "🎁 Подарки", },
        { "value": "food", "display": "🍏 Продукты питания", },
        { "value": "meds", "display": "💊 Лекарства", },
        { "value": "communication", "display": "📱 Связь", },
        { "value": "software", "display": "🎮 Софт, игры", },
        { "value": "tech", "display": "💻 Техника", },
        { "value": "transport", "display": "🚗 Транспорт", },
        { "value": "hobby", "display": "🎨 Хобби и творчество", },
        { "value": "salary", "display": "💼 Зарплата", },
        { "value": "fee", "display": "💲 Гонорар", },
        { "value": "find", "display": "💲 Находка", },
        { "value": "ecommerce", "display": "💰 Э-коммерция", },
        { "value": "crowdfunding", "display": "💖 Краудфандинг", },
        { "value": "interest", "display": "💵 Проценты от банков", },
        { "value": "trading", "display": "📈 Трейдинг", },
        { "value": "other", "display": "❓ Прочее" },
    ];
    
    @override Widget build(BuildContext context)
    {
        return Scaffold(
            appBar: AppBar(title: Text("Новая транзакция"),),
            body: Padding(
                padding: const EdgeInsets.all(16.0),
                child: form(context),
            ),
            resizeToAvoidBottomPadding: false,
        );
    }

    Widget form(context)
    {
        return Form(
            key: _formKey,
            child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                    TextFormField(
                        decoration: const InputDecoration(hintText: "Описание",),
                        validator: (value)
                        {
                            if (value == null || value.isEmpty)
                                return "Введите описание транзакции";
                            _formKey.currentState.save();
                            return null;
                        },
                        onSaved: (String value) {
                            setState(() {
                                _description = value;
                            });
                        },
                    ),
                    Padding(
                        padding: const EdgeInsets.symmetric(vertical: 8.0),
                        child: DropDownFormField(
                            titleText: "Категория",
                            value: _category,
                            validator: (value)
                            {
                                if (value == null || value.isEmpty)
                                    return "Выберите категорию";
                                _formKey.currentState.save();
                                return null;
                            },
                            onSaved: (value) {
                                setState(() {
                                    _category = value;
                                });
                            },
                            onChanged: (value) {
                                setState(() {
                                    _category = value;
                                });
                            },
                            dataSource: _categories,
                            textField: "display",
                            valueField: "value",
                        ),
                    ),
                    Padding(
                        padding: const EdgeInsets.symmetric(vertical: 8.0),
                        child: TextFormField(
                            decoration: const InputDecoration(hintText: "Сумма",),
                            keyboardType: TextInputType.numberWithOptions(decimal: true),
                            validator: (value)
                            {
                                if (value == null || value.isEmpty)
                                    return "Введите сумму";
                                _formKey.currentState.save();
                                return null;
                            },
                            onSaved: (String value) {
                                setState(() {
                                    _value = double.parse(value);
                                });
                            },
                        ),
                    ),
                    Padding(
                        padding: const EdgeInsets.symmetric(vertical: 8.0),
                        child: FlatButton(
                            onPressed: ()
                            {
                                DatePicker.showDateTimePicker(context,
                                    showTitleActions: true,
                                    onChanged: (dt) {
                                        print('change $dt');
                                    },
                                    onConfirm: (dt) {
                                        print('confirm $dt');
                                        datetime = dt;
                                    },
                                    currentTime: DateTime.now(),
                                    locale: LocaleType.ru
                                );
                            },
                            child: Text(
                                "Время и дата",
                                style: TextStyle(color: Colors.blue),
                            ),
                        ),
                    ),
                    Padding(
                        padding: const EdgeInsets.symmetric(vertical: 16.0),
                        child: RaisedButton(
                            onPressed: () async
                            {
                                if (_formKey.currentState.validate())
                                {
                                    await addTransaction();
                                    Navigator.pop(context);
                                }
                            },
                            child: Text("Создать"),
                        ),
                    ),
                ],
            ),
        );
    }
    
    addTransaction() async
    {
        final dt = datetime ?? new DateTime.now();
        final trans = WalletTransaction(
            description: _description,
            category: _category,
            currency: widget.account.currency,
            value: _value,
            accountId: widget.account.id,
            datetime: dt.toIso8601String(),
        );
        return WalletDatabase.db.insertTransaction(trans);
    }
}
