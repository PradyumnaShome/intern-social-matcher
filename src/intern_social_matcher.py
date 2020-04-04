import itertools
import random
import sys
import os
import json
import csv
from collections import defaultdict

COMMON_FIELD = "common_attributes"
INTERESTS_FIELD = "interests"


def preprocess_data(input_filename):
    """
    Takes in a a CSV file with interns and useful information, and generates a list of objects which comprise all the fields for a person.
    """
    intern_list = []
    with open(sys.argv[1]) as intern_list_file:
        csv_reader = csv.DictReader(intern_list_file)
        for index, row in enumerate(csv_reader):
            if index == 0:
                pass
            intern_list.append(row)
        return intern_list


def generate_intern_pairings(intern_list, group_size):
    """
    Partitions the given list of interns into groups of given size.
    """
    random.shuffle(intern_list)

    intern_count = len(intern_list)
    return [intern_list[x : x + group_size] for x in range(0, intern_count, group_size)]


def intersect_n_lists(lists):
    """
    Returns a set containing elements that are common across all lists in the containing list passed in to this function.
    """
    assert lists
    intersection = set(lists[0])
    sets = [set(list_) for list_ in lists]
    for _set in sets:
        intersection = intersection & _set

    return intersection


def preprocess_interests(match):
    """
    Replaces the comma-delimited interests list, with a list of interests, and accumulates them across everyone in the group.
    Every interest is normalized, to ensure duplicates are not accidentally overcounted later.
    @param match - A group of interns that were matched together.
    @returns List of interest lists for each person in the matched group.
    """
    list_of_interest_lists = [person[INTERESTS_FIELD].split(",") for person in match]
    normalized_list = [
        [normalize_word(item) for item in interest_list]
        for interest_list in list_of_interest_lists
    ]
    return normalized_list


def find_common_attributes(list_of_interest_lists):
    """
    @param list_of_interest_lists - A list of all interests that everyone in the match has.
    @return match_object - The given match_object, with a populated common attributes field.
    If there is an interest shared by everyone in the match, it is added to the common interest list.
    Otherwise, a few random interests that one or more people have, are added to the common interest list.
    """
    DESIRED_COMMON_INTEREST_COUNT = 5

    intersection = intersect_n_lists(list_of_interest_lists)

    flattened_interest_list = [
        item for interest_list in list_of_interest_lists for item in interest_list
    ]

    unassigned_interests = set(flattened_interest_list)
    common_interests = set()

    if intersection:
        for item in intersection:
            common_interests.add(item)
            unassigned_interests.remove(item)

    # In case there are less than DESIRED_COMMON_INTEREST_COUNT common interests, and new interests left to choose from,
    # we pick random topics to talk about that aren't necessarily common interests

    while (
        unassigned_interests and len(common_interests) < DESIRED_COMMON_INTEREST_COUNT
    ):
        # Cannot index into set, so temporarily work on list representation
        item = random.choice(list(unassigned_interests))
        common_interests.add(item)
        unassigned_interests.remove(item)

    return list(common_interests)


def normalize_word(word):
    return word.strip().lower()


def is_multiple_value_field(field):
    """
    Checks if a particular field can have multiple values.
    E.g. A list of a user's interests, past employers etc.
    """
    return field in [INTERESTS_FIELD]


def postprocess_match(input_match):
    """
    Builds an object for one matched group of interns, containing two fields "matches" and COMMON_FIELD.
        "matches" is equivalent to the input_match argument - a list of intern objects that is essentially the JSON representation of each CSV record.
        COMMON_FIELD is a field containing a list of strings which represent anything common between the interns.
    @param input_match - An object with a list of interns that were matched.
    @return The enhanced match object, ready for rendering.
    """
    assert input_match

    processed_match = defaultdict(list)
    processed_match["matches"] = input_match

    all_fields = input_match[0].keys()

    # Represents fields that contain just one element, as opposed to a field like interests
    single_item_fields = defaultdict(list)
    for field in all_fields:
        # We would like to consolidate the interns' interests here.
        if is_multiple_value_field(field):
            # Assumption: This field is an interests list.
            # Right now, that is the only multiple value field we're handling.
            # This can be made more generic in the future.
            list_of_interest_lists = preprocess_interests(input_match)
            common_interests = find_common_attributes(list_of_interest_lists)
            processed_match[COMMON_FIELD] += common_interests
        else:
            # Accumulate all the values for a field in the matched group
            for person in input_match:
                single_item_fields[field].append(normalize_word(person[field]))

    # Find more commonalities for single value fields, e.g. school.
    for single_item_field, value in single_item_fields.items():
        for item in value:
            if value.count(item) > 1 and item not in processed_match[COMMON_FIELD]:
                processed_match[COMMON_FIELD].append(item)

    if "" in processed_match[COMMON_FIELD]:
        processed_match[COMMON_FIELD].remove("")

    return processed_match


def postprocess_matches(matches):
    """
    Add interesting information.
    If there is an interest shared by 2 or more members (or if not randomly choose a few items), make it show up here.
    """
    return [postprocess_match(match) for match in matches]


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "See usage in README. Must provide path to file with a CSV file of intern information, group size, and output file.",
            file=sys.stderr,
        )
        sys.exit(os.EX_USAGE)

    input_filename = sys.argv[1]
    intern_list = preprocess_data(input_filename)

    group_size = int(sys.argv[2])
    matches = generate_intern_pairings(intern_list=intern_list, group_size=group_size)

    postprocessed_matches = postprocess_matches(matches)

    output_serialized = json.dumps(postprocessed_matches, indent=4, sort_keys=True)

    output_filename = sys.argv[3]
    with open(output_filename, "w") as output_file:
        output_file.write(output_serialized)
