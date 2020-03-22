import "package:flutter/material.dart";
import "./confirmDialog.dart";
import "./account.dart";
import "./database.dart";

class WalletAccountDetails extends StatefulWidget
{
    final WalletAccount account;
    WalletAccountDetails({Key key, this.account}): super(key: key);
    @override WalletAccountDetailsState createState() => WalletAccountDetailsState();
}


class WalletAccountMenuItem
{
    final String title;
    const WalletAccountMenuItem({this.title});
}

final List<WalletAccountMenuItem> _menuItems = <WalletAccountMenuItem>[
    const WalletAccountMenuItem(title: "Удалить"),
];

class WalletAccountDetailsState extends State<WalletAccountDetails>
{
    //final _formKey = GlobalKey<FormState>();
    void _menuSelect(WalletAccountMenuItem item) async
    {
        await confirmDialog(
            context: context,
            onUserAction: (ConfirmAction action) {
                if (action == ConfirmAction.ACCEPT)
                {
                    print("delete");
                    // TODO: delete account
                    WalletDatabase.db.deleteAccount(widget.account);
                    Navigator.pop(context);
                }
                else
                {
                    //
                }
            }
        );
    }

    Widget menu()
    {
        return PopupMenuButton<WalletAccountMenuItem>(
            onSelected: _menuSelect,
            itemBuilder: (BuildContext context) {
                return _menuItems.map((WalletAccountMenuItem item) {
                    return PopupMenuItem<WalletAccountMenuItem>(
                        value: item,
                        child: Text(item.title),
                    );
                }).toList();
            },
        );
    }

    @override Widget build(BuildContext context)
    {
        return Scaffold(
            appBar: AppBar(
                title: Text(widget.account.name),
                actions: <Widget>[menu(),],
            ),
            body: Padding(
                padding: const EdgeInsets.all(16.0),
                child: form(context),
            ),
        );
    }

    Widget form(context)
    {
        return Center(child: Text("No data"));
    }
}
