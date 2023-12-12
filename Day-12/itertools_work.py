#
# Adding in this interesting approach to part 1 that
# uses `itertools` to the max. Not my coriginal code but
# modified to hemlp my exploration
#
# https://www.reddit.com/user/NikitaSkybytskyi/ 
# https://www.reddit.com/r/adventofcode/comments/18gqqbh/2023_day_12_part_1_solved_in_under_three_minutes/
#
import itertools

def match(records: str, nums: list[int]) -> bool:
    # groupby will take
    # `##.#...` and make
    # [ ('#' ['#', '#']), ('.' ['.']), (# ['#']), ('.', ['.', '.', '.']) ]
    # grouping the consecutive characters
    # if key keeps only the # groups
    # sum adds 1 for each # producing [2, 1]
    # compare that with the nums we were looking for, return True if it maches

    return nums == [
        sum(1 for _ in grouper)
        for key, grouper in itertools.groupby(records)
        if key == "#"
    ]

def brute_force(records: str, nums: list[int]) -> int:
    # gen is a tuple of all the chars, replacing '?' with '#.' its replacements
    # '?.#' -> ('#.', '.', '#')
    gen = ("#." if letter == "?" else letter for letter in records)

    # product(*gen) will decompose the tuple and produce the matching of all the
    #   tuple elements, 
    # producing all the possible combinations of wild card substitutions
    # ('#.', '.', '#') -> [('#', '.', '#'), ('.', '.', '#')]

    # for each candidate, call the above match to see if it's a match
    # for our sequnce (nums). Sum all the True to get all combinations
    return sum(match(candidate, nums) for candidate in itertools.product(*gen))


record = '????.#...#...'
for key, grouper in itertools.groupby(record):
     print(f'{key} {[x for x in grouper]}')
#print(record)
#print(brute_force(record, [4,1,1]))