#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
typedef uint8_t BUFFER;
void createJPEG(FILE *inputFile, int *filenum);
int main(int argc, char *argv[])
{
    // error with return 1 if not just 1 argument is entered
    if (argc != 2)
    {
        printf("Usage; ./recover FILE\n");
        return 1;
    }
    // open file and set to read
    FILE *card = fopen(argv[1], "r");
    // return 1 if the file cannot be opened
    if (card == NULL)
    {
        printf("Could not read file\n");
        return 1;
    }
    int *filenum = malloc(sizeof(int));
    if (filenum == NULL)
    {
        printf("Could not assign memory for file number\n");
    }
    *filenum = -1;
    // while data is still in the memory card, create jpegs from the data
    createJPEG(card, filenum);
    // createJPEG(card, buffer, filenum, blocksize);

    // free(buffer);
    free(filenum);
    fclose(card);
    // close the files
    return 0;
}

void createJPEG(FILE *inputFile, int *filenum)
{
    char filename[8];
    // if (filename == NULL)
    // {
    //     printf("failed to assign memory for filename\n");
    //     return;
    // }
    FILE *img;
    uint8_t buffer[512];
    while (fread(buffer, 1, 512, inputFile) == 512)
    {
        // printf("%x\n", buffer[0]);
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (*filenum == -1)
            {
                *filenum += 1;
                sprintf(filename, "%03i.jpg", *filenum);
                img = fopen(filename, "w");
                fwrite(buffer, 1, 512, img);
            }
            else
            {
                fclose(img);
                *filenum += 1;
                sprintf(filename, "%03i.jpg", *filenum);
                img = fopen(filename, "w");
                fwrite(buffer, 1, 512, img);
            }
        }
        else if (*filenum > -1)
        {
            fwrite(buffer, 1, 512, img);
        }
    }
    fclose(img);
    // free(filename);
    return;
}
