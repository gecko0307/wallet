import "package:flutter/material.dart";

enum ConfirmAction { CANCEL, ACCEPT }

Future<ConfirmAction> confirmDialog({
    BuildContext context,
    @required void Function(ConfirmAction action) onUserAction,
}) async
{
    return showDialog<ConfirmAction>(
        context: context,
        barrierDismissible: false,
        builder: (BuildContext context)
        {
            return AlertDialog(
                title: Text("Удалить счет?"),
                content: const Text("Это действие не может быть отменено"),
                actions: <Widget>[
                    FlatButton(
                        child: const Text("Нет"),
                        onPressed: () {
                            Navigator.of(context).pop(ConfirmAction.CANCEL);
                            onUserAction(ConfirmAction.CANCEL);
                        },
                    ),
                    FlatButton(
                        child: const Text("Да"),
                        onPressed: () {
                            Navigator.of(context).pop(ConfirmAction.ACCEPT);
                            onUserAction(ConfirmAction.ACCEPT);
                        },
                    )
                ],
            );
        },
    );
}
