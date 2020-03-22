import "package:flutter/material.dart";
import "package:dropdown_formfield/dropdown_formfield.dart";
import "./database.dart";
import "./account.dart";

class WalletAddAccount extends StatefulWidget
{
    WalletAddAccount({Key key}): super(key: key);
    @override WalletAddAccountState createState() => WalletAddAccountState();
}

class WalletAddAccountState extends State<WalletAddAccount>
{
    final _formKey = GlobalKey<FormState>();
    String _name = "";
    String _currency = "";
    String _description = "";

    @override Widget build(BuildContext context)
    {
        return Scaffold(
            appBar: AppBar(title: Text("Новый счет"),),
            body: Padding(
                padding: const EdgeInsets.all(16.0),
                child: form(context),
            ),
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
                        decoration: const InputDecoration(hintText: "Название",),
                        validator: (value)
                        {
                            if (value.isEmpty)
                            return "Введите название счета";
                            _formKey.currentState.save();
                            return null;
                        },
                        onSaved: (String value) {
                            setState(() {
                                _name = value;
                            });
                        },
                    ),
                    Padding(
                        padding: const EdgeInsets.symmetric(vertical: 8.0),
                        child: DropDownFormField(
                            titleText: "Валюта",
                            value: _currency,
                            onSaved: (value) {
                                setState(() {
                                    _currency = value;
                                });
                            },
                            onChanged: (value) {
                                setState(() {
                                    _currency = value;
                                });
                            },
                            dataSource: [
                                {
                                    "display": "Российский рубль",
                                    "value": "RUB",
                                },
                                {
                                    "display": "Доллар США",
                                    "value": "USD",
                                },
                                {
                                    "display": "Евро",
                                    "value": "EUR",
                                },
                            ],
                            textField: "display",
                            valueField: "value",
                        ),
                    ),
                    Padding(
                        padding: const EdgeInsets.symmetric(vertical: 8.0),
                        child: TextFormField(
                            decoration: const InputDecoration(hintText: "Описание",),
                            validator: (value)
                            {
                                _formKey.currentState.save();
                                return null;
                            },
                            onSaved: (String value) {
                                setState(() {
                                    _description = value;
                                });
                            },
                        ),
                    ),
                    Padding(
                        padding: const EdgeInsets.symmetric(vertical: 16.0),
                        child: RaisedButton(
                            onPressed: () async
                            {
                                if (_formKey.currentState.validate())
                                {
                                    await addAccount(_name, _currency, _description);
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

    addAccount(String name, String currency, String description) async
    {
        final acc = WalletAccount(
            name: name,
            description: description,
            currency: currency,
        );
        return await WalletDatabase.db.insertAccount(acc);
    }
}
