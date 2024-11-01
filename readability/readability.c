#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

string sentence;
int count_length(string text);
int count_letters(string text, int length);
int count_words(string text, int length);
int count_sentence(string text, int length);

int main(void)
{
    int length;

    sentence = get_string("Text: ");
    //  printf("%s\n", sentence);
    length = count_length(sentence);
    //  printf("%i letters\n", count_letters(sentence, length));
    //  printf("%i words\n", count_words(sentence, length));
    //  printf("%i sentences\n", count_sentence(sentence, length));
    //  average number of letters over 100 words
    float L = (float) count_letters(sentence, length) / count_words(sentence, length) * 100;
    // printf("%f\n", L);
    //  average number of sentences over 100 words
    float S = (float) count_sentence(sentence, length) / count_words(sentence, length) * 100;
    // printf("%f\n", S);
    float index = 0.0588 * L - 0.296 * S - 15.8;
    index = round(index);
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index > 15)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %.0f\n", index);
    }
}

int count_letters(string text, int length)
{
    int count = 0;
    int i;
    for (i = 0; i < length; i++)
    {
        if ((text[i] >= 65 && text[i] <= 90) || (text[i] >= 97 && text[i] <= 122))
        {
            count++;
        }
    }
    return count;
}

int count_words(string text, int length)
{
    int wordcount = 0;
    int lettercount = 0;
    int i;
    for (i = 0; i < length + 1; i++)
    {
        if ((text[i] == 32 || text[i] == 3 || text[i] == 0) && lettercount > 0)
        {
            wordcount++;
            lettercount = 0;
        }
        else if ((text[i] >= 65 && text[i] <= 90) || (text[i] >= 97 && text[i] <= 122))
        {
            lettercount++;
        }
    }
    return wordcount;
}

int count_length(string text)
{
    int length;
    length = strlen(text);
    return length;
}

int count_sentence(string text, int length)
{
    int count = 0;
    int i;
    for (i = 0; i < length + 1; i++)
    {
        if ((text[i] == 33 || text[i] == 46 || text[i] == 63))
        {
            count++;
        }
    }
    return count;
}
