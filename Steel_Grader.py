# This is a sample Python script.
import pandas as pa
import re
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def load_element_grades():
    try:
        grade_data = pa.read_excel("Steel Grade Info.xlsx",sheet_name="Grades",usecols = 'A:M')
        print("Steel grades loaded successfully!")
    except:
        print("Steel grades could not be loaded!")
    return grade_data.set_index("Steel Grade ").to_dict('index')


def load_sample_info():
    try:
        sample_data = pa.read_excel("Steel Grade Info.xlsx", sheet_name="Samples", usecols='A:M')
        print("Steel Samples loaded successfully!")
    except:
        print("Steel Samples could not be loaded!")
    return sample_data.set_index("Steel Grade Samples").to_dict('index')





def check_elements(curr_grade, desired_grade, current_weight):
    # create a dictionary of current element weights using percentages
    current_elem_weights = {}

    for i in curr_grade:
        current_elem_weights[i] = curr_grade[i] * current_weight

    new_elem_weights = current_elem_weights.copy()

    elements_to_be_added = {}

    # iterate through all elements and find which need to be added and how much should be added
    elements_not_equal = True
    while(elements_not_equal):
        count = 0
        for q in curr_grade:
            if curr_grade[q] == desired_grade[q] :
                count+=1
        if count == len(curr_grade):
            # print the percentages after element addition and return
            print("New Percentages: ")
            for p in curr_grade:
                print(p, '-', round(curr_grade[p], 5) * 100, '%')
            print(round(sum(curr_grade.values()), 3) * 100)
            return elements_to_be_added, curr_grade

        for j in current_elem_weights:
            if curr_grade[j] < desired_grade[j]:
                while curr_grade[j] < desired_grade[j]:

                    #if the element does not exist within the current sample
                    if curr_grade[j] == 0.0:
                        new_elem_weights[j] =+ 1
                        curr_grade[j] = round(new_elem_weights[j] / sum(new_elem_weights.values()),5)
                        for l in curr_grade:
                            curr_grade[l] = round(new_elem_weights[l] / sum(new_elem_weights.values()),5)

                    #adds weight based on the ratio
                    new_elem_weights[j] = round(desired_grade[j]/curr_grade[j]*new_elem_weights[j],5)

                    #updates percentages distibutions
                    for l in curr_grade:
                        curr_grade[l] = round(new_elem_weights[l] / sum(new_elem_weights.values()),5)

                    #adds elements and thier corresponding weights
                    elements_to_be_added[j] = round(new_elem_weights[j] - current_elem_weights[j], 5)

            #if iron percentage falls below the grade there is no solution
            #elif curr_grade[j] < desired_grade[j] and j == 'Fe':
                #print(curr_grade[j])
                #return {'None': 0}, curr_grade


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    grade_list = load_element_grades()
    sample_list = load_sample_info()
    print('the following steel grades have been loaded:')
    print('-------------------------------------------------')
    for k in grade_list:
        print("Steel grade", k)
    print('-------------------------------------------------', "\n")
    print('the following samples have been loaded:')
    print('-------------------------------------------------')
    for h in sample_list:
        print(h)
    print('-------------------------------------------------', "\n")

    while(True):
        grade_name = int(input("Enter a valid Steel Grade:"))
        if grade_name not in grade_list:
            print('invalid name!')
            continue
        sample_name = input("Enter a valid Sample Name:")
        if sample_name not in sample_list:
            print('invalid name!')
            continue
        init_weight = float(input("Enter the weight of the steel in Grams:"))

        #check for contamination



        elements_to_add,percentages = check_elements(sample_list[sample_name], grade_list[int(grade_name)], init_weight)


        #if production is not possible
        if 'None' in elements_to_add:
            print('Production of Steel grade not possible!')
            continue
        else:
            print('----------------------NEEDED ELEMENTS------------------------', "\n")
            for e in elements_to_add:
                print(e,' - ',elements_to_add[e],'g')
            init_weight += round(sum(elements_to_add.values()))
            print('Final Weight: ',init_weight ,'g')
            break



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
