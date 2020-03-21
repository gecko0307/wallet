import "package:flutter/material.dart";
import "./wallet/home.dart";

void main() => runApp(WalletApp());

class WalletApp extends StatelessWidget
{
  @override Widget build(BuildContext context)
  {
    return MaterialApp(
      title: "Flutter Demo",
      theme: ThemeData(primarySwatch: Colors.green),
      home: WalletHome(title: "Wallet 2"),
    );
  }
}
