"""
Design two functions, the first function converts a list of strings into one string and returns this string. The second function receives this string and converts it back to the original list of strings. We assume all the special characters are possible inside input strings. Please note that the return of the first function can only be one single string. But you are free to add any extra characters you want inside the return string to help the second function do the separation. 


["*a.bc", "1$24", "12", "1w"] -> code -> original 
"""

# Solution: Use this format for code: "3-4-2-1..abc1234121"

def list_to_code(list_string):
    lengths = '-'.join([str(len(string)) for string in list_string])
    code_string = lengths + '.' + ''.join(list_string)
    return code_string

def code_to_list(code_string):
    lists = code_string.split('.', 1)
    # breakpoint()
    locations = [int(i) for i in lists[0].split('-')] # [3, 4, 2, 1]
    strings = lists[1]
    list_string = []
    cur_loc = 0
    for l in locations:
        list_string.append(strings[cur_loc:cur_loc+l])
        cur_loc += l
    return list_string


code = list_to_code(['.111', '$2', '.'])
print(code)
string = code_to_list(code)
print(string)
