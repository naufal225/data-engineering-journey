amounts = [15000,20000,5000]

total = 0

for amount in amounts:
    total += amount
    
print(total)

high_value_orders = []

for amount in amounts:
    if amount > 10000:
        high_value_orders.append(amount)

print(high_value_orders)

raw_amounts = ["15000", "20000", "0", "500"]

clean_amounts = []
total = 0

for value in raw_amounts:
    amount = int(value)
    if amount > 0:
        clean_amounts.append(amount)
        total += amount

print(clean_amounts)
print("total:",total)

