#include <cs50.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

long cardnumber(void);
bool iseven(int n);
void creditcardinfo(void);
int evennumgeneration(int j);
int main(void)
{

    creditcardinfo();
    // int j;
    // int n;
    // int evennum = 0;
    // do{
    // n = get_int("enter initial integer ");
    //         j = n / 10;
    //         printf("value of j = %i\n", j);
    //         j = n - (j * 10);
    //         printf("value of SECOND j = %i\n", j);
    // evennum = evennumgeneration(j);
    // printf("test result is %i\n", evennum);
    // }
    // while(n > -1);
}

void creditcardinfo(void)
{
    //  check if mastercard (starts with 51, 52, 53, 54, 55 AND is 16 digits long)
    //  check if visa (starts with 4, AND is either 13 OR 16 digits long)
    //  check if AMEX (starts with 34 or 37 AND is 15 digits long)
    //  starting from the second last digit, multiply by 2, then add up each digit (0-9), add up every other digit
    //  starting from the last digit, add up every other digit
    //  add the two numbers together, if the last digit is 0, it's valid

    //  storing the card number
    long cardnum = cardnumber();
    //  making a version of the card number which can be updated throughout the loop
    long n = cardnum;
    //  storing the sum of all odd numbers
    int oddnum = 0;
    //  storing the sum of all even numbers
    int evennum = 0;
    //  storing the added even and odd numbers
    int totalnum;
    //  used to get the length of the card number
    int len;
    //  storing the value to determine the card type
    int cardtype;

    for (len = 0; n > 1; len++)
    {
        //  getting the current right most digit
        int j = n / 10;
        j = n - (j * 10);

        //  printf("j value = %i\n", j);
        //  checking if the digit is even or odd
        if (iseven(len + 1))
        {
            evennum += evennumgeneration(j);
            // if(j / 10 == 0)
            // {
            //     evennum += j * 2;
            // }
            // else
            // {
            //     evennum += j / 10 *2;
            //     evennum += (j - (j / n * 10)) * 2;
            // }
            //  printf("evenum update to %i\n", evennum);
        }
        else
        {
            oddnum += j;
            //  printf("oddnum update to %i\n", oddnum);
        }

        if ((len == 15) && (j == 5))
        {
            cardtype = cardtype / 10;
            cardtype += j * 10;
            // printf("value of j for card = %i\n", j);
            // printf("cardtype value = %i\n", cardtype);
        }
        else if ((len == 15) && (j == 4))
        {
            cardtype = j;
            //  printf("cardtype value = %i\n", cardtype);
        }
        else if (len == 14)
        {
            cardtype += j * 10;
            // printf("value of j for card = %i\n", j);
            // printf("cardtype value = %i\n", cardtype);
        }
        else if (len == 13)
        {
            cardtype = j;
            //  printf("cardtype value = %i\n", cardtype);
        }

        else if (len == 12)
        {
            cardtype = j;
            //  printf("cardtype value = %i\n", cardtype);
        }

        n = n / 10;

        //  printf("loop # %i\n", len);
    }

    totalnum = evennum + oddnum;
    printf("Final evennum = %i, oddnum = %i, totalnumber = %i\n", evennum, oddnum, totalnum);
    char buffer[20];
    //  string to print out type of card (VISA / MASTERCARD / AMEX / INVALID)
    char *cardvalidity = buffer;

    if (totalnum - ((totalnum / 10) * 10) != 0)
    {
        cardvalidity = strcpy(cardvalidity, "INVALID");
    }
    else if ((cardtype == 4) && ((len == 13) || (len == 16)))
    {
        cardvalidity = strcpy(cardvalidity, "VISA");
    }
    else if (((cardtype == 34) || (cardtype == 37)) && (len == 15))
    {
        cardvalidity = strcpy(cardvalidity, "AMEX");
    }
    else if (((cardtype == 51) || (cardtype == 52) || (cardtype == 53) || (cardtype == 54) || (cardtype == 55)) && (len == 16))
    {
        cardvalidity = strcpy(cardvalidity, "MASTERCARD");
    }
    else
    {
        cardvalidity = strcpy(cardvalidity, "INVALID");
    }

    //  printf("Number of digits is %i\n", len);

    //  char buffer[len];

    //  sprintf(buffer, "%li", cardnum);
    printf("Number: %li\n", cardnum);
    printf("%s\n", cardvalidity);

    //  printf("third number is %s\n", third);

    // long j = n / 10;
    // int k = n - (j * 10);
    // char s = string printf("%li", n);

    // long len = size_t strlen(s);

    // printf("card number is %li\n", n);
    // printf("divided number is %li\n", j);
    // printf("removed digit is %i\n", k);
    // printf("number of digits is %li\n", len);
}

long cardnumber(void)
{
    long n;
    // do
    // {
    n = get_long("Enter Credit Card Number ");
    // }
    // while ((n < 4000000000000 || n > 5699999999999999));
    return n;
}

bool iseven(int n)
{
    bool even;

    if (n - ((n / 2) * 2) == 0)
    {
        even = true;
    }
    else
    {
        even = false;
    }

    //  printf("result = %i\n", even);
    return even;
}
int evennumgeneration(int j)
{
    j = j * 2;
    int evennum = 0;
    if (j < 10)
    {
        evennum += j;
        //  printf("first evennum = %i\n", evennum);
    }
    else
    {
        evennum += j / 10;
        //  printf("first evennum = %i\n", evennum);
        evennum += (j - ((j / 10) * 10));
        //  printf("last evennum = %i\n", evennum);
    }
    return evennum;
}
