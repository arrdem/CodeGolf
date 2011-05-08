#!/usr/bin/env python
"""
Equilibrium index of a sequence is an index such that the sum of 
elements at lower indexes is equal to the sum of elements at higher 
indexes. 
For example, in a sequence A:
    A[0]=-7 A[1]=1 A[2]=5 A[3]=2 A[4]=-4 A[5]=3 A[6]=0

3 is an equilibrium index, because:
    A[0]+A[1]+A[2]=A[4]+A[5]+A[6]

6 is also an equilibrium index, because:
    A[0]+A[1]+A[2]+A[3]+A[4]+A[5]=0

(sum of zero elements is zero) 7 is not an equilibrium index, 
because it is not a valid index of sequence A.
The idea is to create a program that given a sequence (array), returns 
its equilibrium index (any) or -1 if no equilibrium indexes exist.
"""
i=input()
print[x for x in range(len(i))if sum(i[0:x])==sum(i[x+1::])]
