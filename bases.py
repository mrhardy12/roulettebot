zeroes = [0, "00"]
table = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
    [13, 14, 15],
    [16, 17, 18],
    [19, 20, 21],
    [22, 23, 24],
    [25, 26, 27],
    [28, 29, 30],
    [31, 32, 33],
    [34, 35, 36]
]
reds = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
blacks = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
lows = list(range(1, 19))
highs = list(range(19, 37))
low_dozen = list(range(1, 13))
mid_dozen = list(range(13, 25))
high_dozen = list(range(25, 37))
odds = [i for i in range(1, 37) if i % 2 == 1]
evens = [i for i in range(1, 37) if i % 2 == 0]