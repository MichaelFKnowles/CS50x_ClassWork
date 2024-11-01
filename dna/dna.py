import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Missing command-line arguement")
        sys.exit(0)

    # TODO: Read database file into a variable
    keys, database = streamCSV(sys.argv[1])
    # print(len(keys))
    # print(len(database))
    # print(len(database))
    # TODO: Read DNA sequence file into a variable
    dnaSequence = streamTXT(sys.argv[2])
    # print(dnaSequence)
    # TODO: Find longest match of each STR in DNA sequence

    # TODO: Check database for matching profiles

    for i in range(len(database)):
        for j in range(1, len(keys)):
            count = longest_match(dnaSequence, keys[j])
            if (int(database[i].get(keys[j])) != count):
                break
            elif ((int(database[i].get(keys[j])) == count) and (j == len(keys) - 1)):
                print(database[i].get('name'))
                return
    print("No Match")

    return


def findDNACount(dnaSequence, key):
    DNACount = longest_match(dnaSequence, key)
    return (DNACount)


def streamCSV(input):
    rows = []
    keys = []
    with open(input, newline='') as file:
        reader = csv.DictReader(file)
        # for fieldnames in reader:
        #     rows
        keys = reader.fieldnames
        # print(reader.fieldnames)
        for row in reader:
            rows.append(row)
    # print(rows)
    return (keys, rows)


def streamTXT(input):
    with open(input) as file:
        reader = file.read()
    return (reader)


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
