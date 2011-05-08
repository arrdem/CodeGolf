#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]) {
    if(argc == 1){
        printf("c\n");
        return 0;
    }

    size_t l = strlen(argv[1]);
    int i;
    size_t currentSequence = 0;
    size_t totalDefects = 0;
    size_t lastDefects = 0;

    for(i = l-1; i >= 0; i--){
        if(argv[1][i] == 'E' || argv[1][i] == 'R'){
            totalDefects++;
            currentSequence = 0;
        } else if(argv[1][i] == 'S') {
            currentSequence++;
        }
    }

    if(currentSequence < totalDefects)
        // continue defect sequence
        printf("t\n");
    else if(argv[1][0] == 'S' || argv[1][0] == 'E' ||
            argv[1][1] == 'S' || argv[1][1] == 'E')
        // blind cooperation
        printf("c\n");
    else if(argv[1][0] == 'R')
        // start new defect sequence
        printf("t\n");
    else
        printf("c\n");

    return 0;
}
