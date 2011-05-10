#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

#define THRESHOLD 7
#define RAND 32

int main(int c, char * a []) {
    int r;
    char * x;
    int d = 0;

    srandom(time(0) + getpid());

    if (c == 1) {
        printf("c\n");
        return 0;
    }

    for (x = a[1]; *x; x++)
        if (*x == 'R' || *x == 'E') d++;

    if (d > THRESHOLD || random() % 1024 < RAND || strlen(a[1]) == 99)
        printf("t\n");
    else
        printf("c\n");

    return 0;
}
