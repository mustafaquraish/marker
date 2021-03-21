'''
Python sample student solution for demo-ing the automarker
'''

from time import sleep
from sys import exit

def square(N):
  return N*N

def sum_of_squares(N):
  sum = 0
  for i in range(N+1):
    sum += square(i)
  return sum

def sleep_10_sec():
  sleep(10)

def exit_with_7():
  exit(7)