import numpy as np


def create_matrix(n):
    matrix = []

    for x in range(0, n):
        matrix.append([])

    return matrix


def create_dict(input_):
    my_list = list(input_)
    my_dict = dict.fromkeys(my_list, [])
    my_dict_keys = my_dict.keys()

    return my_dict


def rename_duplicates(keyword_):
    seen = {}
    for x in keyword_:
        if x in seen:
            seen[x] += 1
            yield "%s%d" % (x, seen[x])

        else:
            seen[x] = 0
            yield x


alphabet = "XBCQRLMTEPZSDKUWNGAHYVIFO"
alphabet_np = np.array(list(alphabet))
alphabet_np = alphabet_np.reshape(5, 5)
adfgx_list = ["A", "D", "F", "G", "X"]
adfgvx_list = ["A", "D", "F", "G", "V", "X"]
input_ = "XXGFXGXGDXXDXDXG"

# input_ = "GGGXXXXFDXDGDXXX"
keyword_ = "KOLOTOC"




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



def decode():
    keyword_renamed = list(rename_duplicates(keyword_))
    keyword_renamed_sorted = sorted(keyword_renamed)
    keyword_length = len(keyword_renamed)
    keyword_indices = []
    input_list = list(input_)
    step_count = 0
    output_list = []


    # create input matrix
    input_matrix = create_matrix(keyword_length)

    # fill matrix with characters
    for x in range(0, len(input_list)):
        input_matrix[x % keyword_length].append(input_list[x])

    # create input dict
    input_dict = create_dict(keyword_renamed_sorted)

    # add matrix values to dictionary
    for x in input_dict.keys():
        input_dict[x] = input_matrix[step_count]
        step_count += 1

    for x in range(0, keyword_length):
        keyword_indices.append(keyword_renamed_sorted.index(keyword_renamed[x]))


    input_dict_keys = input_dict.keys()

    for x in keyword_indices:
        print(x)
        print(input_matrix[x])
        output_list.append(input_matrix[x])


    transposed_text = ""
    for x in output_list:
        for y in x:
            transposed_text += y

    # print(reverse_substitution(transposed_text, alphabet_np, 0))

    subs_text = reverse_substitution(transposed_text, alphabet_np, 0)



    print(f"input: {input_}")
    print(f"input list: {input_list}")
    print(f"keyword: {keyword_}")
    print(f"renamed keyword: {keyword_renamed}")
    print(f"sorted renamed keyword: {keyword_renamed_sorted}")
    print(f"input matrix: {input_matrix}")
    print(f"input dict: {input_dict}")
    print(f"keyword indices: {keyword_indices}")
    print(f"output list: {output_list}")
    print(f"transposed text: {transposed_text}")
    print(f"subs text: {subs_text}")


decode()



