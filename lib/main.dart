import "package:flutter/material.dart";
import "./wallet/home.dart";

void main() => runApp(WalletApp());

final _theme = ThemeData(
    primarySwatch: Colors.blue,
    primaryColor: const Color(0xFF2196f3),
    accentColor: const Color(0xFF2196f3),
    canvasColor: const Color(0xFFfafafa),
    fontFamily: "Roboto",
);

class WalletApp extends StatelessWidget
{
    @override Widget build(BuildContext context)
    {
        return MaterialApp(
            title: "Flutter Demo",
            theme: _theme,
            home: WalletHome(title: "Wallet 2"),
        );
    }
}
