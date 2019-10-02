import matplotlib.pyplot as plt

# 0.99
# 0.97
# 1.00
# 1.00

# 0.98
# 0.93
# 1.00
# 1.00

# 0.97
# 0.89
# 0.99
# 1.00

x = [1, 8, 15, 22]
x2 = [2, 9, 16, 23]
x3 = [3, 10, 17, 24]
x4 = [4, 11, 18, 25]
x5 = [5, 12, 19, 26]

# y_sorting = [0.77, 0.59, 0.77, 0.94]
# y_qgram = [0.57, 0.45, 0.18, 0.84]
# y_canopy = [0.88, 0.88, 0.95, 0.99]
# y_suffixarray = [0.90, 0.94, 0.99, 1.00]
# y_stringmap = [0, 0, 0, 0]


# y_sorting = [0.76, 0.54, 0.76, 0.91]
# y_qgram =  [0.53, 0.41, 0.16, 0.78]
# y_canopy = [0.86, 0.85, 0.93, 0.98]
# y_suffixarray = [0.88, 0.92, 0.99, 0.99]
# y_stringmap = [0, 0, 0, 0]
#
#
# y_sorting = [0.76, 0.47, 0.76, 0.89]
# y_qgram =  [0.50, 0.36, 0.14, 0.71]
# y_canopy = [0.84, 0.84, 0.92, 0.97]
# y_suffixarray = [0.87, 0.90, 0.98, 0.98]
# y_stringmap = [0, 0, 0, 0]
#
#
# y_sorting = [0.96, 0.92, 0.95, 0.99]
# y_qgram = [0.92, 0.89, 0.84, 0.97]
# y_canopy = [0.98, 0.98, 0.99, 1.0]
# y_suffixarray = [0.98, 0.99, 1.0, 1.0]
# y_stringmap = [0, 0, 0, 0]
#
# y_sorting = [0.95, 0.84, 0.95, 0.98]
# y_qgram = [0.88, 0.82, 0.76, 0.93]
# y_canopy = [0.97, 0.97, 0.98, 1.0]
# y_suffixarray = [0.97, 0.98, 1.0, 1.0]
# y_stringmap = [0, 0, 0, 0]
#
# y_sorting = [0.95, 0.76, 0.95, 0.97]
# y_qgram = [0.84, 0.74, 0.68, 0.89]
# y_canopy = [0.96, 0.96, 0.98, 0.99]
# y_suffixarray = [0.97, 0.98, 1.0, 1.0]
# y_stringmap = [0, 0, 0, 0]
#
#
# y_sorting = [82.48, 83.84, 89.65, 82.48 + 83.84]
# y_qgram = [81.97, 18.33, 143.35, 81.97 + 18.33]
# y_canopy = [157.35, 120.07, 437.39, 157.35 + 120.07]
# y_suffixarray = [59.31, 63.30, 94.71, 59.31 + 63.30]
# y_stringmap = [0, 0, 0, 0]
#
# y_sorting = [93.36, 90.82, 101.01, 93.36 + 90.82]
# y_qgram = [81.35, 18.29, 141.46, 81.35 + 18.29]
# y_canopy = [155.07, 119.43, 443.36, 155.07 + 119.43]
# y_suffixarray = [57.63, 63.46, 95.74, 57.63 + 63.46]
# y_stringmap = [0, 0, 0, 0]
#
y_sorting = [92.85, 91.87, 100.88, 92.85 + 91.87]
y_qgram = [80.64, 18.37, 140.62, 80.64 + 18.37]
y_canopy = [151.08, 117.60, 445.55, 151.08 + 117.60]
y_suffixarray = [52.22, 62.35, 97.02, 52.22 + 62.35]
y_stringmap = [0, 0, 0, 0]



plt.bar(x, y_sorting, label='sorting', color='#1d73aa')
plt.bar(x2, y_qgram, label='q-gram', color='#8cbc4f')
plt.bar(x3, y_canopy, label='canopy', color='#f48533')
plt.bar(x4, y_suffixarray, label='suffix-array', color='#7a5892')
plt.bar(x5, y_stringmap, label='string-map', color='#009ab2')

plt.ylabel('blocking time (sec)')
plt.ylim(ymin=0.0)
plt.title('All Duplicate Pairs\nCorruption = 10%')
plt.xticks([3, 10, 17, 24], ['list-1', 'list-2', 'list-3', 'list-1-2'])

plt.legend(loc=9, bbox_to_anchor=(0.5, -0.05), ncol=5)
plt.show()

