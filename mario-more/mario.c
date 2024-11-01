#include <cs50.h>
#include <stdio.h>

int get_size(void);
void print_grid(int size);

int main(void)
{
    int n = get_size();
    print_grid(n);
}

int get_size(void)
{
    int size;
    do
    {
        size = get_int("Size = ");
    }
    while (size < 1 || size > 8);
    return size;
}

void print_grid(int size)
{
    //  need to know the size of the largest entry and create whitespace at the start for the higher rows
    for (int i = 0; i < size; i++)
    {
        int j = size - i;
        int h = i + 1;
        for (int k = 1; k < j; k++)
        {
            printf(" ");
        }
        for (int l = 0; l < h; l++)
        {
            printf("#");
        }
        printf("  ");
        for (int l = 0; l < h; l++)
        {
            printf("#");
        }
        printf("\n");
    }
}