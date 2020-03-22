import "package:flutter/material.dart";
import "package:dropdown_formfield/dropdown_formfield.dart";
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
    String _currency = "";
    double _value = 0.0;
    
    @override Widget build(BuildContext context)
    {
        return Scaffold(
            appBar: AppBar(title: Text("Новая транзакция"),),
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
                        decoration: const InputDecoration(hintText: "Описание",),
                        validator: (value)
                        {
                            if (value.isEmpty)
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
        //final dt = new DateTime.now();
        final trans = WalletTransaction(
            description: _description,
            category: _category,
            currency: _currency,
            value: _value,
            accountId: widget.account.id,
            datetime: "0", //dt.toIso8601String(),
        );
        return WalletDatabase.db.insertTransaction(trans);
    }
}
