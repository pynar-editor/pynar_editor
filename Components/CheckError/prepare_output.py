from difflib import SequenceMatcher
def compare_lines( listed_python_data , selectedList, errorList ):
    select_output = []
    error_line_output = []
    for my_list in selectedList:
        if my_list not in listed_python_data:
            select_output.append(my_list)   
                     
    for my_list2 in errorList:
        if my_list2 not in listed_python_data:
            error_line_output.append(my_list2)
    return select_output, error_line_output

def replace_from_list(result_list , select_output, error_line_output , OriginalStrings, i):
    if select_output[i] == str('_STR_:{}'):
        try:
            find_index = (result_list.index(select_output[i]))
            result_list[find_index] = (OriginalStrings[0])
        except:
            pass
    else:    
        find_index = (result_list.index(select_output[i]))
        #result_list = list(map(lambda x: x.replace(result_list[3] , error_line_output[i]), result_list))
        result_list[find_index] = error_line_output[i]
    
    return result_list

def equal_dimensions(result_list , select_output, error_line_output , OriginalStrings):
    for i in range(len(select_output)):        
        result_list = replace_from_list(result_list , select_output, error_line_output , OriginalStrings , i)
    return result_list

def dimension_equalizing(python_word , error_line_output , errorList):
    max_similarity = 0
    for i in error_line_output:
        for j in python_word:
            similarity = SequenceMatcher(None, i, j).ratio()           
            if similarity > max_similarity:
                max_similarity =  similarity
                error_line_word  = i
                python_line_word = j          
    new_errorList = list(map(lambda x: x.replace( error_line_word , python_line_word), errorList))   
    return new_errorList

def check_orginal_string(result_list , OriginalStrings):
    sayac_OriginalStrings = 0
    for i in range(len(result_list)):
        if result_list[i] == "_STR_":
            result_list[i] = OriginalStrings[sayac_OriginalStrings]
            sayac_OriginalStrings+=1
    return result_list          


def my_alliagment_fonc( selectedList , errorList , listed_python_data , OriginalStrings):    
    
    result_list = selectedList.copy()  
    select_output, error_line_output = compare_lines(listed_python_data,selectedList, errorList)        
    if len(select_output) == len(error_line_output): #boyların aynı olduğu durum
        result_list = equal_dimensions(result_list , select_output, error_line_output , OriginalStrings)
    else:                                            #boyların farklı olduğu durum   
        try:
            new_errorList = dimension_equalizing(listed_python_data , error_line_output , errorList)
            select_output_second_turn, error_line_output_second_turn = compare_lines(listed_python_data ,selectedList, new_errorList)         
            if len(select_output_second_turn) == len(error_line_output_second_turn): #boyların aynı olduğu durum
                result_list = equal_dimensions(result_list , select_output_second_turn, error_line_output_second_turn , OriginalStrings)
            else:                                            #boyların farklı olduğu durum
                new_errorList = dimension_equalizing(listed_python_data , error_line_output_second_turn , errorList)
                select_output_thirth_turn, error_line_output_thirth_turn = compare_lines(listed_python_data , selectedList, new_errorList)     
                if len(select_output_thirth_turn) == len(error_line_output_thirth_turn): #boyların aynı olduğu durum
                    result_list = equal_dimensions(result_list , select_output_thirth_turn, error_line_output_thirth_turn , OriginalStrings)
        except NameError:
            pass
    if len(OriginalStrings) > 0:
        result_list = check_orginal_string(result_list , OriginalStrings)
    
    
    return result_list           