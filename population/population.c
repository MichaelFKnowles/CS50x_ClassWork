#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n;
    do
    {
        n = get_int("Enter starting population = ");
    }
    while (n < 9);

    int j;
    do
    {
        j = get_int("Enter target ending population = ");
    }
    while (j < n);

    int years = 0;

    if (n == j)
    {
    }
    else
        do
        {
            n = n + (n / 3) - (n / 4);
            years++;
        }
        while (n < j);
    printf("Years: %i\n", years);
}
