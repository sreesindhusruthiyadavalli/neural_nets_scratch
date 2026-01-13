def dot_product(A, B):
    # Check if multiplication is possible
    if len(A[0]) != len(B):
        raise ValueError("Columns of A must match rows of B")
    
    result = []
    for i in range(len(A)):           # iterate over rows of A
        row_result = []
        for j in range(len(B[0])):    # iterate over columns of B
            sum_product = 0
            for k in range(len(B)):   # iterate over rows of B / columns of A
                sum_product += A[i][k] * B[k][j]
            row_result.append(sum_product)
        result.append(row_result)
    return result


def eye(n, m=None, k=0):
    if m is None:
        m = n
    matrix = []
    for i in range(n):
        row = []
        for j in range(m):
            if j == i + k:
                row.append(1)
            else:
                row.append(0)
        matrix.append(row)
    return matrix


# Dot product example
A = [[1, 4], [5, 6]]
B = [[2, 4], [5, 2]]
print(dot_product(A, B))
# Output: [[22, 12], [40, 32]]

# Eye function example
print(eye(3))
# Output:
# [[1, 0, 0],
#  [0, 1, 0],
#  [0, 0, 1]]
