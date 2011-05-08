A=input()
print[i for i in range(len(A))if sum(A[:i])==sum(A[i+1:])]or-1
