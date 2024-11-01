#include <stdio.h>

int main(void)
{
    int counter = 3;
    while (counter > 0)
    {
        printf("meow\n");
        counter--;
    }

    int i = 0;
    while (i < 3)
    {
        printf("woof\n");
        i++;
    }

    for (int n = 0; n < 3; n++)
    {
        printf("ribbit\n");
    }

}