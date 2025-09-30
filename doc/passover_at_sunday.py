from collections import Counter
import matplotlib.pyplot as plt
from hdate import hdate
from hdate import molad
import numpy as np

begin, end = 5000, 5999
weekdays = []
for year in range(begin, end):
    the_day = hdate.HDate(15, "ניסן", year)
    weekdays.append(molad.Months.weekday(the_day))

yearlen = [molad.Months.year_days(year) for year in range(begin, end)]

# First histogram: count occurrences of weekdays
weekday_counts = Counter(weekdays)
labels = list(range(1, 8))
weekdays_names = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
weekday_values = [weekday_counts.get(i, 0) for i in labels]

# Second histogram: count differences
diffs = np.diff(np.where(np.array(weekdays) == 1)).squeeze()
diff_counts = Counter(diffs)
diff_labels = sorted(diff_counts.keys())
diff_values = [diff_counts[i] for i in diff_labels]

# Create the subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

# First plot: weekdays
colors = plt.cm.rainbow([i / 7 for i in range(7)])
ax1.bar(weekdays_names, weekday_values, color=colors)
ax1.set_title(
    f'Passover Occurrences per Weekday in {end-begin} years({begin}-{end})')
ax1.set_xlabel('Day of Week')
ax1.set_ylabel('# Occurrences')

# Second plot: differences
ax2.bar(diff_labels, diff_values, color='skyblue')
ax2.set_title(
    f'Difference Between Consecutive Passovers@Sunday in {end-begin} years({begin}-{end})')
ax2.set_xlabel('Difference [Years]')
ax2.set_ylabel('Occurrences')
ax2.set_xticks(diff_labels)  # Only integer ticks that actually appear


# Third plot: differences
ax3.bar(range(len(diffs)), diffs, color='skyblue')
ax3.set_title(
    f'Difference Between Consecutive Passovers@Sunday in {end-begin} years({begin}-{end})')
ax3.set_ylabel('Difference [Years]')
ax3.plot(range(len(diffs)), diffs, marker='o', color='red', markersize=10)


plt.tight_layout()
plt.show()
