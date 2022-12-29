import master_data

raw_long = master_data.long
raw_short = master_data.short

long = []
short = []

for i in raw_long:
    long.append(f"NSE:{i}-EQ")

for i in raw_short:
    short.append(f"NSE:{i}-EQ")

symbols = long + short