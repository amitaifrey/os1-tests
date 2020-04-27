#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Bad usage\n");
        return -1;
    }

    int timeout = atoi(argv[1]);

    for (int i = 0; i < timeout; i += 2)
    {
        printf("%d\n", i);
        sleep(2);
    }

    printf("Done: %d\n", timeout);

    return 0;
}
