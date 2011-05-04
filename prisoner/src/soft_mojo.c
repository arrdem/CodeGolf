#include <stdio.h>
#include <string.h>

int main(int argc, char * argv[]) {
    int d = 0, i, l;

    if (argc == 1) {
        printf("c\n");
    } else {
        l = strlen(argv[1]);

        for (i = 0; i < l; i++)
            if (argv[1][i] == 'R' || argv[1][i] == 'E')
                d++;

        printf("%c\n", d > l/2 ? 't' : 'c');
    }
}
