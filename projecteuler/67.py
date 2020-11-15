rows = values.split("\n")
matrix = [list(map(int, r.split())) for r in rows if r]
while len(matrix) > 1:
    last_row = matrix[-1]
    largest_values_from_last_row = [max(pairs) for pairs in zip(last_row, last_row[1:])]
    one_before_last = matrix[-2]
    new_row = [sum(aggregate_values) for aggregate_values in zip(one_before_last, largest_values_from_last_row)]
    matrix.pop()
    matrix[-1] = new_row
print(matrix[0])
