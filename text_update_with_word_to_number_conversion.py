"""This program converts numbers written in words into actual numbers."""
from json import load
from sys import argv
import codecs
from re import sub


def load_json_file(file_path):
    """Load json file into an object."""
    dict_loaded = load(codecs.open(file_path, 'r', 'utf-8'))
    return dict_loaded


def find_consecutive_indexes_and_determine_numeric_value(indexes, numbers):
    """Find consecutive indexes of numbers in words in a sentence and determine its final numeric value."""
    consecutive_indexes = [indexes[0]]
    final_numbers = list()
    select_indexes = [0]
    for i in range(len(indexes) - 1):
        if indexes[i + 1] - indexes[i] == 1:
            consecutive_indexes.append(indexes[i + 1])
            select_indexes.append(i + 1)
        else:
            if len(consecutive_indexes) == 1:
                final_numbers.append((consecutive_indexes[-1], numbers[i], 1))
                select_indexes = [i + 1]
            else:
                intermediate_numbers = list()
                for j in range(select_indexes[0], select_indexes[0] + len(consecutive_indexes)):
                    if numbers[j] == 0:
                        intermediate_numbers.append(numbers[j])
                    elif (numbers[j] in range(1, 10) or numbers[j] in range(11, 20)) and numbers[j + 1] % 100 == 0:
                        intermediate_numbers.append(numbers[j] * numbers[j + 1])
                    elif numbers[j] in [20, 30, 40, 50, 60, 70, 80, 90] and numbers[j + 1] in range(1, 10):
                        intermediate_numbers.append(numbers[j] + numbers[j + 1])
                    elif (numbers[j] in range(1, 19) or numbers[j] in [20, 30, 40, 50, 60, 70, 80, 90]) and (numbers[j - 1] % 100 == 0):
                        intermediate_numbers.append(numbers[j])
                final_number = sum(intermediate_numbers)
                final_numbers.append((consecutive_indexes[0], final_number, len(consecutive_indexes)))
            consecutive_indexes = [indexes[i + 1]]
            select_indexes = [i + 1]
    if not final_numbers and len(consecutive_indexes) == 1:
        final_numbers.append((consecutive_indexes[-1], numbers[-1], 1))
    elif final_numbers and final_numbers[-1][0] != consecutive_indexes[-1] and len(consecutive_indexes) == 1:
        final_numbers.append((consecutive_indexes[-1], numbers[-1], 1))
    else:
        intermediate_numbers = list()
        for j in range(select_indexes[0], select_indexes[0] + len(consecutive_indexes)):
            if numbers[j] == 0:
                intermediate_numbers.append(numbers[j])
            elif j < len(numbers) - 1 and (numbers[j] in range(1, 10) or numbers[j] in range(11, 20)) and numbers[j + 1] % 100 == 0:
                intermediate_numbers.append(numbers[j] * numbers[j + 1])
            elif j < len(numbers) - 1 and numbers[j] in [20, 30, 40, 50, 60, 70, 80, 90] and numbers[j + 1] in range(1, 10):
                intermediate_numbers.append(numbers[j] + numbers[j + 1])
            elif (numbers[j] in range(1, 19) or numbers[j] in [20, 30, 40, 50, 60, 70, 80, 90]) and (numbers[j - 1] % 100 == 0):
                intermediate_numbers.append(numbers[j])
        final_number = sum(intermediate_numbers)
        final_numbers.append((consecutive_indexes[0], final_number, len(consecutive_indexes)))
    return final_numbers


def convert_word_expression_to_number(text, dict_word_number):
    """Convert an expression in words into a number."""
    text = sub('[-]', ' ', text)
    print(text)
    words = text.split()
    number_index = list()
    list_numbers = list()
    final_words = list()
    # handle floats
    for index, word in enumerate(words):
        retrieved_number = change_word_to_number(word.lower(), dict_word_number)
        if retrieved_number:
            number_index.append(index)
            list_numbers.append(retrieved_number)
        elif word == 'and' and change_word_to_number(words[index - 1], dict_word_number) and change_word_to_number(words[index + 1], dict_word_number):
            number_index.append(index)
            list_numbers.append(0)
    if number_index:
        final_numbers = find_consecutive_indexes_and_determine_numeric_value(number_index, list_numbers)
        start, end = 0, len(words)
        for ind, number, length in final_numbers:
            final_words += words[start: ind] + [str(number)]
            start = ind + length
        if start == end:
            pass
        else:
            final_words += words[start: end]
    else:
        final_words = words
    return ' '.join(final_words)


def change_word_to_number(word, dict_word_number):
    """
    Retrieve the number if word is found in the word2Number mapping.

    Args:
    word - word to be searched
    dict_word_number - mapping containing word and
                         its corresponding number
    Returns:
    retrieved number
    """
    if word in dict_word_number:
        return dict_word_number[word]
    elif word[: -1] in dict_word_number:
        return dict_word_number[word[: -1]]
    else:
        return None


def main():
    """
    Pass main arguments and call the functions.

    Args:

    Returns:
    """
    text = argv[1]
    json_file = argv[2]
    loaded_object = load_json_file(json_file)
    print(convert_word_expression_to_number(text, loaded_object))


if __name__ == '__main__':
    main()
