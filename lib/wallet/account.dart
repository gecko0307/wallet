class WalletAccount
{
  final int id;
  final String name;
  final String description;
  final String currency;

  WalletAccount({this.id, this.name, this.description, this.currency});

  Map<String, dynamic> toMap()
  {
    return
    {
      "name": name,
      "description": description,
      "currency": currency,
    };
  }

  static fromMap(Map<String, dynamic> map)
  {
    return WalletAccount(
      id: map["id"],
      name: map["name"],
      description: map["description"],
      currency: map["currency"],
    );
  }
}
