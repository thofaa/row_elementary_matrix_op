import numpy as np
import re
import sys

np.set_printoptions(precision=4, suppress=True)  

def main_algorithm():
    while True:
        try:
            print('')
            print('Type "-1" to exit and end the program')
            num_system = int(input('How many equations that you have? : ').strip())

            if num_system == -1:
                sys.exit()
            else:
                break

        except ValueError:
            print('Your input number of equation is not suitable!')

    equation_system = np.empty((0,1)) #initial matrix for equation input
    num_equation = 0 #make a ordinal sequence for input
    max_num_variable = 0 #make a maximum number of variable that exist

    for m in range(num_system):
        num_equation += 1

        #endswith method to check whether a component belong to other component
        if num_equation in [11, 12, 13]: 
            ordinal_sys = 'th'
        elif str(num_equation).endswith('1'): 
            ordinal_sys = 'st'
        elif str(num_equation).endswith('2'): 
            ordinal_sys = 'nd'
        elif str(num_equation).endswith('3'): 
            ordinal_sys = 'rd'
        else: 
            ordinal_sys = 'th'

        y = input(f'Input your {num_equation}{ordinal_sys} equation: ')

        nonspace_equation = ''
        for char in y:
            if not char.isspace():
                nonspace_equation += char

        equation_system = np.append(arr=equation_system, values=[[nonspace_equation]], axis=0) #stack vertically
        
        check_variable = re.findall(string=nonspace_equation, pattern=r'\_(\d+)') #find gretest index variable
        for el in check_variable:
            if int(el) > max_num_variable:
                max_num_variable = int(el)

    into_main_matrix = np.zeros((num_system, max_num_variable + 1))  # +1 for augmented column (right side)

    for i in range(num_system): #iteration based on row matrix
        check_right_side = re.findall(string=equation_system[i][0], pattern=r'=(\-?\d+\.?\d*)') #fetch right side value only
        check_value = re.findall(string=equation_system[i][0], pattern=r'(\-?\d*\.?\d*)\D+\_(\d+)') #fetch all digit number, not include right side value

        for m in range(len(check_value)): #row of pairs of two tuple element: [(x,y),...]
            index_coeff = int(check_value[m][1]) - 1
            value_coeff = check_value[m][0]
            if value_coeff == '':
                into_main_matrix[i][index_coeff] = 1 #input one into matrix
            elif value_coeff == '-':
                into_main_matrix[i][index_coeff] = -1 #input negative one into matrix
            else:
                into_main_matrix[i][index_coeff] = float(value_coeff) #input coeff commonly except both condition above

        for el in check_right_side: #input right side value into matrix
            into_main_matrix[i][-1] = float(el)

        into_initial_matrix = into_main_matrix.copy() #to display it later, user has to know about it!

    def square_matrix():
        nonlocal into_main_matrix  # allow modification of outer variable
        check_shape = into_main_matrix.shape
        main_diagonal = np.zeros((1,check_shape[1]-1)) #the right hand side value doesn't include in the main diagonal

        #check null value of diagonal first, URGENT!
        for i in range(check_shape[0]):
            if into_main_matrix[i][i] == float(0):
                change_null_value = 0
                for j in range(check_shape[0]):
                    if into_main_matrix[j][i] != float(0):
                        change_null_value = into_main_matrix[j][i]
                        break #this loop will be break for it has got first non null value
                into_main_matrix[i][i] = change_null_value

        for i in range(check_shape[0]): 
            main_diagonal[0][i] = into_main_matrix[i][i] #index diagonal is always same when the matrix is square

            diagonal_func = 1/main_diagonal[0][i]
            into_main_matrix[i] = into_main_matrix[i]*diagonal_func #operate all row element based on the function

            for m in range(check_shape[0]):
                if m != i:
                    factor = into_main_matrix[m][i]  #the coefficient to eliminate, this will be never change for the elimination happened
                    into_main_matrix[m] = into_main_matrix[m] - factor * into_main_matrix[i]

        #Clean up tiny floating-point
        into_main_matrix = np.where(np.abs(into_main_matrix) < 1e-10, 0, into_main_matrix)
        into_main_matrix = np.round(into_main_matrix, 3)

    check_shape = into_main_matrix.shape
    if check_shape[0] == (check_shape[1] - 1):
        square_matrix()
        print('')
        print('your initial matrix:')
        print(into_initial_matrix)
        print('')
        print('the final result matrix:')
        print(into_main_matrix)
    else:
        print(f'we have not provide an algorithm to solve nonsquare matrix\
              \nyour matrix shape: {check_shape}')

while True:
    main_algorithm()

    