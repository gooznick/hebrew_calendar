from hdate.molad import (
    Months,
    YEARS_PATTERNS_LEAP,
    YEARS_PATTERNS_NON_LEAP,
)
from hdate.gematria import MONTHS_LEAP, str_to_num, num_to_str

import copy
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


month_days = [30, 29, 29, 29, 30, 29, 0, 0, 30, 29, 30, 29, 30, 29]

# prepare the dictionary 
dates = {}
for month  in range(14):
    for day in range(30):
        dates.setdefault((month, day), set())

def update_dates(dates, months, current_day):
    for month, days in enumerate(months):
        for day in range(days):
            val = dates.setdefault((month, day), set())
            val.add(current_day % 7)
            current_day = current_day + 1

for pattern in YEARS_PATTERNS_NON_LEAP:
    specific_month_days = copy.copy(month_days)
    if pattern[1] == "ש":
        specific_month_days[1] += 1
        specific_month_days[2] += 1
    elif pattern[1] == "כ":
        specific_month_days[2] += 1

    update_dates(dates, specific_month_days, str_to_num(pattern[0]))
month_days = [30, 29, 29, 29, 30, 0, 29, 30, 30, 29, 30, 29, 30, 29]
for pattern in YEARS_PATTERNS_LEAP:
    specific_month_days = copy.copy(month_days)
    if pattern[1] == "ש":
        specific_month_days[1] += 1
        specific_month_days[2] += 1
    elif pattern[1] == "כ":
        specific_month_days[2] += 1
    update_dates(dates, specific_month_days, str_to_num(pattern[0]))

# remove empty 
dates = {k:v for k,v in dates.items() if v}

months_names = copy.copy(MONTHS_LEAP)
months_names.insert(5, "אדר")
months_names[6] = "אדר א'"

# Convert to readable
pattern_per_date = {}
for k, v in dates.items():
    pattern = "".join([num_to_str(vv if vv != 0 else 7) for vv in v][::-1])
    date = f"{num_to_str(k[1]+1)[::-1]} {months_names[k[0]]}"[::-1]
    pattern_per_date[date] = pattern


# Graph
labels = [" ".join(date.split()[:-1]) + "א' "[::-1] for date in pattern_per_date.keys()]
y = [len(v) for v in pattern_per_date.values()]
x = range(len(labels))
change_idx = [0] + [
    i for i in range(1, len(labels))
    if labels[i] != labels[i - 1]
]
tick_labels = [str(labels[i]) for i in change_idx]
plt.figure(figsize=(10, 4))
plt.plot(x, y, marker="o")  # no custom colors/styles per your requirement
plt.gca().invert_xaxis()
plt.xticks(change_idx, tick_labels, rotation=45, ha="right")
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.grid(axis="x", which="major")
plt.xlabel("תאריך"[::-1])
plt.ylabel("מספר הימים בהם יכול לחול"[::-1])
plt.title("מספר ימי השבוע בהם יכול לחול תאריך"[::-1])
plt.tight_layout()
plt.show()
