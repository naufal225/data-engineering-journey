order_id = 1
amount = 200000.0
status = "PAID"
is_valid = True

# Cek tipe data

print(type(order_id))
print(type(amount))
print(type(status))
print(type(is_valid))

# Type Casting

amount = "12000"
amount = int(amount)

print(amount)

price = "199.9"
price = float(price)

print(price)

order_id = 2
order_id = str(order_id)

print(order_id)

amount = "12,000"
# amount = int(amount) # error
amount = amount.replace(",", "")
amount = int(amount)
print(amount)