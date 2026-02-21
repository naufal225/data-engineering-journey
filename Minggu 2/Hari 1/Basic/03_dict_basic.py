order = {"id":"1","amount":"12000"}

print(order["amount"])
print(order.get("amount"))

amount = order.get("amount", 0) # <- versi aman

print(order.keys()) 
print(order.values()) ## biar tau struktur dan nilai nya

## ubah nilai dict

amount = int(order["amount"])
order["amount"] = amount
order["is_valid"] = True ## nambah item

print(order)
