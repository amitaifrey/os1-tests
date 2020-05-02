#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
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
        std::cout << i << std::endl;
        sleep(2);
    }

    std::cout << "Done: " << timeout << std::endl;

    return 0;
}
