#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Must be one number and base\n");
        return 1;
    }


    int base = atol(argv[2]);
    char *num_value = argv[1];
    char *temp;
    if (base == 16)
    {
    printf("%li\n", strtol(num_value, &temp, base));
    return 0;
    }
    else if (base == 10)
    {
        int i = 1, j, k = 0, tmp;
        char hex_num_tmp[100];
        int number = atol(num_value);

        while (number != 0)
        {
            tmp = number % 16;
            printf("%i\n", tmp);
            if(tmp < 10)
            {
                tmp = tmp + 48;
            }
            else
            {
                tmp = tmp + 55;
            }
            hex_num_tmp[i++] = tmp;
            number = number / 16;
        }

        char hex_num[i];
        for(j = i - 1; j > 0; j--)
        {
            hex_num[k] = hex_num_tmp[j];
            printf("j = %c\n", hex_num_tmp[j]);
            k++;
        }
        printf("%s", hex_num);
        printf("\n");
        return 0;

    }
    else
    {
        printf("Must enter 10 for convert to int or 16 for convert to hex");
        return 1;
    }
    return 0;
}
