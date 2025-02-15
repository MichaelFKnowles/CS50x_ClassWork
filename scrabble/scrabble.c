#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);
string convertToUppercase(string word);

int main(void)
{
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    convertToUppercase(word1);
    convertToUppercase(word2);

    int score1 = compute_score(word1);
    // printf("Player 1: %i\n", score1);
    int score2 = compute_score(word2);
    // printf("Player 2: %i\n", score2);

    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!");
    }
}

int compute_score(string word)
{
    int points = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        int letternum = word[i] - 65;
        printf("n value %i\n", letternum);
        if (letternum >= 0 && letternum <= 26)
        {
            points += POINTS[letternum];
        }
    }
    return points;
}

string convertToUppercase(string word)
{
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        word[i] = toupper(word[i]);
    }
    return word;
}