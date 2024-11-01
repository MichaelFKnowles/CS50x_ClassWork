#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // FILE *file = fopen("debug.txt", "w");
    // if (file == NULL)
    // {
    //     return;
    // }
    // fprintf(file, "%i, %i, %x\n", height, width, image[0][300].rgbtGreen);
    // fprintf(file, "%i, %i, %x\n", height, width, image[height][width].rgbtBlue);
    int blue = 0, green = 0, red = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // blue = hextoint(image[i][j].rgbtBlue);
            // green = hextoint(image[i][j].rgbtGreen);
            // red = hextoint(image[i][j].rgbtRed);
            blue = image[i][j].rgbtBlue;
            green = image[i][j].rgbtGreen;
            red = image[i][j].rgbtRed;
            int average = round((blue + green + red) / 3.0);
            // fprintf(file, "blue %i, green %i, red %i, average %i\n", blue, green, red, average);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE reflect[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            reflect[i][width - 1 - j].rgbtBlue = image[i][j].rgbtBlue;
            reflect[i][width - 1 - j].rgbtGreen = image[i][j].rgbtGreen;
            reflect[i][width - 1 - j].rgbtRed = image[i][j].rgbtRed;
        }
        for (int k = 0; k < width; k++)
        {
            image[i][k].rgbtBlue = reflect[i][k].rgbtBlue;
            image[i][k].rgbtGreen = reflect[i][k].rgbtGreen;
            image[i][k].rgbtRed = reflect[i][k].rgbtRed;
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // FILE *file = fopen("debug.txt", "w");
    // if (file == NULL)
    // {
    //     return;
    // }
    RGBTRIPLE blur[height][width];
    int blue = 0, green = 0, red = 0, average = 0;
    float count = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            count = 0;
            blue = image[i][j].rgbtBlue;
            green = image[i][j].rgbtGreen;
            red = image[i][j].rgbtRed;
            count++;
            if (i - 1 >= 0)
            {
                if (j - 1 >= 0)
                {
                    blue += image[i - 1][j - 1].rgbtBlue;
                    green += image[i - 1][j - 1].rgbtGreen;
                    red += image[i - 1][j - 1].rgbtRed;
                    count++;
                }
                blue += image[i - 1][j].rgbtBlue;
                green += image[i - 1][j].rgbtGreen;
                red += image[i - 1][j].rgbtRed;
                count++;
                if (j + 1 < width)
                {
                    blue += image[i - 1][j + 1].rgbtBlue;
                    green += image[i - 1][j + 1].rgbtGreen;
                    red += image[i - 1][j + 1].rgbtRed;
                    count++;
                }
            }
            if (i >= 0 && i < height)
            {
                if (j - 1 >= 0)
                {
                    blue += image[i][j - 1].rgbtBlue;
                    green += image[i][j - 1].rgbtGreen;
                    red += image[i][j - 1].rgbtRed;
                    count++;
                }
                if (j + 1 < width)
                {
                    blue += image[i][j + 1].rgbtBlue;
                    green += image[i][j + 1].rgbtGreen;
                    red += image[i][j + 1].rgbtRed;
                    count++;
                }
            }
            if (i + 1 < height)
            {
                if (j - 1 >= 0)
                {
                    blue += image[i + 1][j - 1].rgbtBlue;
                    green += image[i + 1][j - 1].rgbtGreen;
                    red += image[i + 1][j - 1].rgbtRed;
                    count++;
                }
                blue += image[i + 1][j].rgbtBlue;
                green += image[i + 1][j].rgbtGreen;
                red += image[i + 1][j].rgbtRed;
                count++;
                if (j + 1 < width)
                {
                    blue += image[i + 1][j + 1].rgbtBlue;
                    green += image[i + 1][j + 1].rgbtGreen;
                    red += image[i + 1][j + 1].rgbtRed;
                    count++;
                }
            }
            average = round(blue / count);
            // fprintf(file, "blue %i, average %i\n", blue, average);
            blur[i][j].rgbtBlue = average;
            // fprintf(file, "New blue %i, Old blue %i\n", blur[i][j].rgbtBlue, image[i][j].rgbtBlue);
            average = round(green / count);
            // fprintf(file, "green %i, average %i\n", green, average);
            blur[i][j].rgbtGreen = average;
            // fprintf(file, "New green %i, Old green %i\n", blur[i][j].rgbtGreen, image[i][j].rgbtGreen);
            average = round(red / count);
            // fprintf(file, "red %i, average %i\n", red, average);
            blur[i][j].rgbtRed = average;
            // fprintf(file, "New red %i, Old red %i\n", blur[i][j].rgbtRed, image[i][j].rgbtRed);

            // fprintf(file, "Count: %i || New BGR %i %i %i || Old BGR %i %i %i\n", count, blur[i][j].rgbtBlue,
            // blur[i][j].rgbtGreen, blur[i][j].rgbtRed, image[i][j].rgbtBlue, image[i][j].rgbtGreen, image[i][j].rgbtRed);
        }
    }
    for (int k = 0; k < height; k++)
    {
        for (int l = 0; l < width; l++)
        {
            image[k][l].rgbtBlue = blur[k][l].rgbtBlue;
            image[k][l].rgbtGreen = blur[k][l].rgbtGreen;
            image[k][l].rgbtRed = blur[k][l].rgbtRed;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // FILE *file = fopen("debug.txt", "w");
    // if (file == NULL)
    // {
    //     return;
    // }
    RGBTRIPLE edges[height][width];

    int gxb = 0, gxg = 0, gxr = 0, gyb = 0, gyg = 0, gyr = 0, bsqrt, gsqrt, rsqrt;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            gxb = 0;
            gxg = 0;
            gxr = 0;
            gyb = 0;
            gyg = 0;
            gyr = 0;
            if (i - 1 >= 0)
            {
                if (j - 1 >= 0)
                {
                    gxb += -1 * image[i - 1][j - 1].rgbtBlue;
                    gxg += -1 * image[i - 1][j - 1].rgbtGreen;
                    gxr += -1 * image[i - 1][j - 1].rgbtRed;
                    gyb += -1 * image[i - 1][j - 1].rgbtBlue;
                    gyg += -1 * image[i - 1][j - 1].rgbtGreen;
                    gyr += -1 * image[i - 1][j - 1].rgbtRed;
                }
                gyb += -2 * image[i - 1][j].rgbtBlue;
                gyg += -2 * image[i - 1][j].rgbtGreen;
                gyr += -2 * image[i - 1][j].rgbtRed;

                if (j + 1 < height)
                {
                    gxb += 1 * image[i - 1][j + 1].rgbtBlue;
                    gxg += 1 * image[i - 1][j + 1].rgbtGreen;
                    gxr += 1 * image[i - 1][j + 1].rgbtRed;
                    gyb += -1 * image[i - 1][j + 1].rgbtBlue;
                    gyg += -1 * image[i - 1][j + 1].rgbtGreen;
                    gyr += -1 * image[i - 1][j + 1].rgbtRed;
                }
            }
            if (i >= 0 && i < height)
            {
                if (j - 1 >= 0)
                {
                    gxb += -2 * image[i][j - 1].rgbtBlue;
                    gxg += -2 * image[i][j - 1].rgbtGreen;
                    gxr += -2 * image[i][j - 1].rgbtRed;
                }
                if (j + 1 < height)
                {
                    gxb += 2 * image[i][j + 1].rgbtBlue;
                    gxg += 2 * image[i][j + 1].rgbtGreen;
                    gxr += 2 * image[i][j + 1].rgbtRed;
                }
            }
            if (i + 1 < height)
            {
                if (j - 1 >= 0)
                {
                    gxb += -1 * image[i + 1][j - 1].rgbtBlue;
                    gxg += -1 * image[i + 1][j - 1].rgbtGreen;
                    gxr += -1 * image[i + 1][j - 1].rgbtRed;
                    gyb += 1 * image[i + 1][j - 1].rgbtBlue;
                    gyg += 1 * image[i + 1][j - 1].rgbtGreen;
                    gyr += 1 * image[i + 1][j - 1].rgbtRed;
                }
                gyb += 2 * image[i + 1][j].rgbtBlue;
                gyg += 2 * image[i + 1][j].rgbtGreen;
                gyr += 2 * image[i + 1][j].rgbtRed;
                if (j + 1 < width)
                {
                    gxb += 1 * image[i + 1][j + 1].rgbtBlue;
                    gxg += 1 * image[i + 1][j + 1].rgbtGreen;
                    gxr += 1 * image[i + 1][j + 1].rgbtRed;
                    gyb += 1 * image[i + 1][j + 1].rgbtBlue;
                    gyg += 1 * image[i + 1][j + 1].rgbtGreen;
                    gyr += 1 * image[i + 1][j + 1].rgbtRed;
                }
            }
            // fprintf(file, "Horizontal blue = %i, green = %i, red = %i ||  ", gxb, gxg, gxr);
            // fprintf(file, "Vertical blue = %i, green = %i, red = %i\n", gyb, gyg, gyr);
            bsqrt = round(sqrt(pow(gxb, 2) + pow(gyb, 2)));
            gsqrt = round(sqrt(pow(gxg, 2) + pow(gyg, 2)));
            rsqrt = round(sqrt(pow(gxr, 2) + pow(gyr, 2)));
            // fprintf(file, "SQUARE ROOT blue = %i, green = %i, red = %i\n", bsqrt, gsqrt, rsqrt);

            if (bsqrt > 255)
            {
                bsqrt = 255;
            }
            if (gsqrt > 255)
            {
                gsqrt = 255;
            }
            if (rsqrt > 255)
            {
                rsqrt = 255;
            }
            edges[i][j].rgbtBlue = bsqrt;
            edges[i][j].rgbtGreen = gsqrt;
            edges[i][j].rgbtRed = rsqrt;
        }
    }

    for (int k = 0; k < height; k++)
    {
        for (int l = 0; l < width; l++)
        {
            image[k][l].rgbtBlue = edges[k][l].rgbtBlue;
            image[k][l].rgbtGreen = edges[k][l].rgbtGreen;
            image[k][l].rgbtRed = edges[k][l].rgbtRed;
        }
    }

    return;
}
