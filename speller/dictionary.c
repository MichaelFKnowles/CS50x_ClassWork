// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "dictionary.h"

// Represents a node in a hash table
// TODO: Choose number of buckets in hash table
const unsigned int N = 27; // added a 26th item for apostrophy

typedef struct node
{
    bool boolIsWord;
    struct node *children[N];
} node;

node *table;
node *createNode();

void freeTrieMemory(node *trie);
unsigned int wordcount = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    node *ptr = table;
    if (ptr == NULL)
    {
        return false;
    }
    for (int i = 0; i < strlen(word); i++)
    {
        int num = hash(&word[i]);
        ptr = ptr->children[num];
        if (ptr == NULL)
        {
            return false;
        }
        else if ((i == strlen(word) - 1) && ptr->boolIsWord)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    char inputWord = word[0];
    inputWord = toupper(inputWord);
    unsigned int letter = inputWord;
    if (letter > 64 && letter < 91)
    {
        return letter - 65;
    }
    else if (letter == 39) // capturing apostrophy
    {
        return 26;
    }
    return 9000; // returns 9000 when no valid character is found
}

bool load(const char *dictionary)
{
    FILE *source = fopen(dictionary, "r");
    if (source == NULL)
    {
        return false;
    }
    table = createNode();
    char letter;
    unsigned int hashNum;
    node *ptr = table;
    unsigned int position = 0;
    while (fread(&letter, sizeof(char), 1, source) != 0)
    {
        hashNum = hash(&letter);
        // printf("letter: %c\nhashNum: %u\n", letter, hashNum);
        if (hashNum == 9000)
        {
            ptr->boolIsWord = true;
            ptr = table;
            wordcount++;
        }
        else
        {
            if (ptr->children[hashNum] == NULL)
            {
                node *n = createNode();
                ptr->children[hashNum] = n;
                ptr = n;
                // free(n);
            }
            else
            {
                ptr = ptr->children[hashNum];
            }
        }
    }

    fclose(source);
    return true;
}

void freeTrieMemory(node *trie)
{
    for (int i = 0; i < N; i++)
    {
        if (trie->children[i] != NULL)
        {
            freeTrieMemory(trie->children[i]);
        }
    }
    free(trie);
}

node *createNode()
{
    node *n = malloc(sizeof(node));
    if (n == NULL)
    {
        return NULL;
    }
    for (int i = 0; i < N; i++)
    {
        n->children[i] = NULL;
    }
    n->boolIsWord = false;

    return n;
}
// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (table == NULL)
    {
        return 0;
    }
    return wordcount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    if (table == NULL)
    {
        return false;
    }
    freeTrieMemory(table);
    return true;
}
