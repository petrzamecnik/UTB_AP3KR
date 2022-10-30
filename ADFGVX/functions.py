import math
import random
import numpy as np
import re
import unidecode

alphabet_full = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
alphabet_reduced = alphabet_full[:-10]
adfgx_list = ["A", "D", "F", "G", "X"]
adfgvx_list = ["A", "D", "F", "G", "V", "X"]
repl_english = [("J", "I")]
repl_czech = [("W", "V")]
repl_czech_specials = [("Č", "C"), ("Ď", "D"), ("Ě", "E"), ("Ň", "N"), ("Ř", "R"), ("Š", "S"), ("Ť", "T"), ("Ž", "Z"),
                       ("Á", "A"), ("É", "E"), ("Í", "I"), ("Ó", "O"), ("Ú", "U"), ("Ů", "U"), ("Ý", "Y")]
repl_numbers = [(" ", "XSPACE"), ("0", "XZERO"), ("1", "XONE"), ("2", "XTWO"), ("3", "XTHRE"),
                        ("4", "XFOUR"), ("5", "XFIVE"), ("6", "XSIX"), ("7", "XSEVEN"), ("8", "XEIGHT"), ("9", "XNINE")]


def tst():
    print(alphabet_full)
    print(alphabet_reduced)


def get_alphabet_full():
    output = []

    for x in alphabet_full:
        output.append(x)

    return output


def get_alphabet_full_np():
    return np.array(get_alphabet_full()).reshape(6, 6)


def get_alphabet_reduced_en():
    output = []
    en = re.sub("J", "", alphabet_reduced)

    for x in en:
        output.append(x)

    return output


def get_alphabet_reduced_cz():
    output = []
    cz = re.sub("Q", "", alphabet_reduced)

    for x in cz:
        output.append(x)

    return output


def get_alphabet_reduced_en_np():
    return np.array(get_alphabet_reduced_en()).reshape(5, 5)


def get_alphabet_reduced_cz_np():
    return np.array(get_alphabet_reduced_cz()).reshape(5, 5)


def get_adfgx_list():
    return adfgx_list


def get_adfgvx_list():
    return adfgvx_list


def parse_keyword(input_, lang):
    output = ""
    input_ = input_.upper()

    if lang == 0:
        for pattern, replacement in repl_english:
            input_ = re.sub(pattern, replacement, input_)

        for pattern, replacement in repl_czech_specials:
            input_ = re.sub(pattern, replacement, input_)

        for x in input_:
            if x in alphabet_reduced:
                output += x

        return output


    elif lang == 1:
        for pattern, replacement in repl_czech:
            input_ = re.sub(pattern, replacement, input_)

        for pattern, replacement in repl_czech_specials:
            input_ = re.sub(pattern, replacement, input_)

        for x in input_:
            if x in get_alphabet_reduced_cz():
                output += x

        return output

    return "WTF"


def parse_input(input_, mode, lang):
    output = []
    input_ = input_.upper()

    # ADFGX
    if mode == 0:
        # EN
        if lang == 0:
            for pattern, replacement in repl_czech_specials:
                input_ = re.sub(pattern, replacement, input_)

            for pattern, replacement in repl_english:
                input_ = re.sub(pattern, replacement, input_)

            for pattern, replacement in repl_numbers:
                input_ = re.sub(pattern, replacement, input_)

            for x in input_:
                if x in get_alphabet_reduced_en():
                    output += x

            return output

        # CZ
        elif lang == 1:
            for pattern, replacement in repl_czech_specials:
                input_ = re.sub(pattern, replacement, input_)

            for pattern, replacement in repl_czech:
                input_ = re.sub(pattern, replacement, input_)

            for pattern, replacement in repl_numbers:
                input_ = re.sub(pattern, replacement, input_)

            for x in input_:
                if x in get_alphabet_reduced_cz():
                    output += x

            return output

    # ADFGVX
    elif mode == 1:
        for pattern, replacement in repl_czech_specials:
            input_ = re.sub(pattern, replacement, input_)

        for x in input_:
            if x in get_alphabet_full():
                output += x

        return output



def create_matrix(n):
    matrix = []

    for x in range(0, n):
        matrix.append([])

    return matrix


def create_dict(input_):
    # my_list = ["K", "O1", "L", "O2", "T", "O3", "C"]
    my_list = list(input_)
    my_dict = dict.fromkeys(my_list, [])
    my_dict_keys = my_dict.keys()

    return my_dict, my_dict_keys


# generators: https://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do
def rename_duplicates(keyword_):
    seen = {}
    for x in keyword_:
        if x in seen:
            seen[x] += 1
            yield "%s%d" % (x, seen[x])

        else:
            seen[x] = 0
            yield x


def transpose(input_, keyword_):
    print("transpose")
    # print(input_)
    # print(keyword_)
    # keyword_ = "KOLOTOC"
    keyword_original = keyword_

    keyword_ = rename_duplicates(keyword_)
    # print(f"keyword with indexex: {list(keyword_)}")

    dict, dict_keys = create_dict(keyword_)

    # input_ = "AHOJPEPOJAKSEMAS"
    input_list = list(input_)
    keyword_count = len(keyword_original)

    input_list_by_keyword_count = create_matrix(keyword_count)

    try:
        # fill matrix with characters
        for x in range(0, len(input_list)):
            input_list_by_keyword_count[x % keyword_count].append(input_list[x])

        print(f"INPUT LIST BY KEYWORD COUNT {input_list_by_keyword_count}")

        step_count = 0
        # add matrix values to dictionary
        for x in dict_keys:
            dict[x] = input_list_by_keyword_count[step_count]
            step_count += 1
    except:
        pass

    # print(f"keyword count: {keyword_count}")
    # print(f"dict: {dict}")
    # print(f"dict_keys: {dict_keys}")
    # print(f"input_list: {input_list}")
    # print(f"list by kw count: {input_list_by_keyword_count}")
    #
    # dict_keys = sorted(dict_keys)
    # print(dict_keys)
    # for x in dict_keys:
    #     print(dict[x])

    return dict, dict_keys


def substitute(input_, alphabet, cipher_mode):
    output = []
    bigram = []
    n = 5  # default
    cipher_chars = ""

    # ADFGX
    if cipher_mode == 0:
        n = 5
        cipher_chars = adfgx_list

    # ADFGVX
    elif cipher_mode == 1:
        n = 6
        cipher_chars = adfgvx_list

    alphabet_np = np.array(alphabet).reshape(n, n)

    # print("ALPHABET ---")
    for x in input_:
        c1 = x
        c1row = np.where(alphabet_np == c1)[0]
        c1col = np.where(alphabet_np == c1)[1]
        output.append(cipher_chars[int(c1row)])
        output.append(cipher_chars[int(c1col)])

    return output


def reverse_substitution(input_, alphabet, cipher_mode):
    output = []
    n = 5  # default
    cipher_chars = ""
    input_to_bigrams = []


    # ADFGX
    if cipher_mode == 0:
        n = 5
        cipher_chars = adfgx_list

    # ADFGVX
    elif cipher_mode == 1:
        n = 6
        cipher_chars = adfgvx_list

    alphabet_np = np.array(alphabet).reshape(n, n)

    for x in range(0, len(input_), 2):
        bigram = []
        bigram.append(input_[x])
        bigram.append(input_[x + 1])
        input_to_bigrams.append(bigram)

    # print(alphabet_np)
    # print(input_to_bigrams)


    for x in range(0, len(input_to_bigrams)):
        bigram = input_to_bigrams[x]
        col = cipher_chars.index(bigram[0])
        row = cipher_chars.index(bigram[1])
        output.append(alphabet_np[row][col])
        # print(f"ROW: {row} | COL: {col}")


    output_string = ""
    for x in output:
        output_string += x
        print(x)


    return output_string


def encode(input_, keyword_, alphabet, cipher_mode):
    print("ENCODE")
    # list after substitution
    print(f"Input: {input_}")
    input_sub = substitute(input_, alphabet, cipher_mode)
    output_text = ""

    # dictionary after transposition
    dict_, dict_keys = transpose(input_sub, keyword_)

    # sorting keys
    sorted_keys = sorted(dict_keys)
    for x in sorted_keys:
        for y in dict_[x]:
            output_text += y

    output_text = add_spaces(output_text, 5)
    print(f"Dict: {dict_} ")
    return output_text



def decode(input_, keyword_, alphabet, cipher_mode):
    print("DECODE")
    output_text = ""
    text_after_transposition = ""
    output_list = []
    input_list = list(input_)
    keyword_original = list(rename_duplicates(keyword_))
    keyword_sorted = list(sorted(rename_duplicates(keyword_)))
    keyword_length = len(keyword_)
    keyword_indices = []

    keyword_renamed = rename_duplicates(keyword_original)

    # create dictionary before transposition
    dict_before_transposition, dict_before_transposition_keys = create_dict(keyword_renamed)

    # create array for each character in keyword
    input_matrix = create_matrix(keyword_length)

    # fill input_array by cipher text
    try:
        # fill matrix with characters
        for x in range(0, len(input_list)):
            input_matrix[x % keyword_length].append(input_list[x])

        step_count = 0
        # add matrix values to dictionary
        for x in dict_before_transposition_keys:
            dict_before_transposition[x] = input_matrix[step_count]
            # print(dict_before_transposition[x])
            step_count += 1

    except:
        pass

    print(f"input_matrix {input_matrix}")
    print(dict_before_transposition)

    for x in range(0, keyword_length):
        keyword_indices.append(keyword_sorted.index(keyword_original[x]))

    print(keyword_indices)

    for x in keyword_indices:
        output_list.append(input_matrix[x])

    for lst in output_list:
        for x in lst:
            text_after_transposition += x



    print(output_list)
    print(f"Text after transposition: {text_after_transposition}")

    output_text = reverse_substitution(text_after_transposition, alphabet, cipher_mode)





    # print(keyword_sorted.index(keyword_original[0]))
    # print(keyword_original[0])
    print(f"keyword original: {keyword_original}")
    print(f"keyword sorted: {keyword_sorted}")
    print(f"keyword length: {keyword_length}")


    # reverse transposition

    print(type(output_text))

    return output_text





def add_spaces(string, length):
    return " ".join(string[i:i + length] for i in range(0, len(string), length))


def remove_spaces(string):
    index = 0
    new_string = ""

    # check if there is space at correct position, if true then remove it
    for x in string:
        if (index % 5 == 0) and index != 0:
            new_string = new_string + ""
            index = 0
        else:
            new_string = new_string + x
            index += 1

    return new_string




# def decode(input_, keyword_, alphabet, cipher_mode):
#     print("DECODE")
#     output_text = ""
#     text_after_transposition = ""
#     output_list = []
#     input_list = list(input_)
#     keyword_original = list(rename_duplicates(keyword_))
#     keyword_sorted = list(sorted(rename_duplicates(keyword_)))
#     keyword_length = len(keyword_)
#     keyword_indices = []
#
#     keyword_renamed = rename_duplicates(keyword_original)
#
#     # create dictionary before transposition
#     dict_before_transposition, dict_before_transposition_keys = create_dict(keyword_renamed)
#
#     # create array for each character in keyword
#     input_matrix = create_matrix(keyword_length)
#
#     # fill input_array by cipher text
#     try:
#         # fill matrix with characters
#         for x in range(0, len(input_list)):
#             input_matrix[x % keyword_length].append(input_list[x])
#
#         step_count = 0
#         # add matrix values to dictionary
#         for x in dict_before_transposition_keys:
#             dict_before_transposition[x] = input_matrix[step_count]
#             # print(dict_before_transposition[x])
#             step_count += 1
#
#     except:
#         pass
#
#     print(f"input_matrix {input_matrix}")
#     print(dict_before_transposition)
#
#     for x in range(0, keyword_length):
#         keyword_indices.append(keyword_sorted.index(keyword_original[x]))
#
#     print(keyword_indices)
#
#     for x in keyword_indices:
#         output_list.append(input_matrix[x])
#
#     for lst in output_list:
#         for x in lst:
#             text_after_transposition += x
#
#
#
#     print(output_list)
#     print(f"Text after transposition: {text_after_transposition}")
#
#     output_text = reverse_substitution(text_after_transposition, alphabet, cipher_mode)
#
#
#
#
#
#     # print(keyword_sorted.index(keyword_original[0]))
#     # print(keyword_original[0])
#     print(f"keyword original: {keyword_original}")
#     print(f"keyword sorted: {keyword_sorted}")
#     print(f"keyword length: {keyword_length}")
#
#
#     # reverse transposition
#
#     print(type(output_text))
#
#     return output_text
