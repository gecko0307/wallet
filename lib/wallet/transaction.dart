class WalletTransaction
{
    final int id;
    final String description;
    final String category;
    final String currency;
    final double value;
    final int accountId;
    final String datetime;

    WalletTransaction({
        this.id,
        this.description,
        this.category,
        this.currency,
        this.value,
        this.accountId,
        this.datetime,
    });

    Map<String, dynamic> toMap()
    {
        return
        {
            "description": description,
            "category": category,
            "currency": currency,
            "value": value,
            "account": accountId,
            "datetime": datetime,
        };
    }

    static fromMap(Map<String, dynamic> map)
    {
        return WalletTransaction(
            id: map["id"],
            description: map["description"],
            category: map["category"],
            currency: map["currency"],
            value: map["value"],
            accountId: map["account"],
            datetime: map["datetime"].toString(),
        );
    }
}
