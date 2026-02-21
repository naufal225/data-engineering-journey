raw_orders = [
    {"id":"1","amount":"15,000","status":"paid"},
    {"id":"2","amount":"0","status":"cancelled"}
]

clean_orders = []

for order in raw_orders:
    amount = int(order["amount"].replace(",",""))
    status = order["status"].upper()
    
    if amount > 0 and status == "PAID":
        clean_orders.append({
            "id": int(order["id"]),
            "amount":amount,
            "status":status
        })
        
print("raw orders:",raw_orders)
print("clean_orders:",clean_orders)