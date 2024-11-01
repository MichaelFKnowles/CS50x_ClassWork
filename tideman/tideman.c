#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void loop_scan(int depth, int loop_candidate_winner, int loop_candidate_loser, int loop_candidate_int);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            //  sets the candidate number in the current rank
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    pair tmp_pairs[2] = {0};
    int tmp_max;
    int flipped = 0;
    for (int i = 0; i < pair_count - 1; i++)
    {
        tmp_pairs[0] = pairs[i];
        tmp_pairs[1] = pairs[i + 1];
        if ((preferences[pairs[i].winner][pairs[i].loser] - preferences[pairs[i].loser][pairs[i].winner]) <
            (preferences[pairs[i + 1].winner][pairs[i + 1].loser] - preferences[pairs[i + 1].loser][pairs[i + 1].winner]))
        {
            flipped = 1;
            pairs[i] = tmp_pairs[1];
            pairs[i + 1] = tmp_pairs[0];
        }
    }

    if (flipped == 1)
    {
        sort_pairs();
    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        locked[pairs[i].winner][pairs[i].loser] = true;
        loop_scan(candidate_count, pairs[i].winner, pairs[i].loser, pairs[i].loser);
    }
    return;
}

void loop_scan(int depth, int loop_candidate_winner, int loop_candidate_loser, int loop_candidate_int)
{
    depth--;
    int detected_loops = 0;
    if (loop_candidate_int == loop_candidate_winner)
    {
        locked[loop_candidate_winner][loop_candidate_loser] = false;
        return;
    }
    else if (depth < 0)
    {
        return;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[loop_candidate_int][i] == true)
        {
            detected_loops++;
            loop_scan(depth, loop_candidate_winner, loop_candidate_loser, i);
        }
    }
    if (detected_loops == 0)
    {
        depth = 0;
        loop_scan(depth, loop_candidate_winner, loop_candidate_loser, loop_candidate_int);
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    int true_counter = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        true_counter = 0;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i] == true)
            {
                true_counter++;
                break;
            }
        }
        if (true_counter == 0)
        {
            printf("%s\n", candidates[i]);
            break;
        }
    }
    return;
}
