#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

int square(int N) {
  return N*N;
}

int sum_of_squares(int N) {
  int sum = 0;
  for (int i = 0; i <= N; i++)
    sum += square(i);
  return sum;
}

void sleep_10_sec() {
  sleep(10);
}

void exit_with_7() {
  exit(7);
}