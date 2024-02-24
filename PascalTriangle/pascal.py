from collections import Counter
from math import ceil

def search_pascal_multiples_fast(row_limit):
    if row_limit<5: #exclude the first 4 rows because there are no values to check
        return []
    else:
        #initialize first row that matters
        pascal_row=[1,4,6,4,1]
        inner_values=[6] #inner values are the numbers in each row excluding the first and last 2 numbers
        #generate each row and extract the inner values of each row
        #(start at row 6)
        for n in range(6, row_limit):
            half_length = ceil((n-2) / 2)
            #only looping through half of the rows because they are symmetrical (the even ones)
            half =  [pascal_row[i] + pascal_row[i + 1] for i in range(half_length)]
            if n % 2 == 0:
                pascal_row[1:n] = half + half[::-1]
            else:
                pascal_row[1:n] = half + half[:-1][::-1]
            
            inner_values.extend(pascal_row[2:n-2])
        
        #count how many times each element appears
        value_counts = Counter(inner_values)
        
        #return the numbers that had appeared more than 3 times
        return sorted([k for k, v in value_counts.items() if v > 3])

def search_pascal_multiples_slow(row_limit):

    # Building up Pascal's triangle with a dict of lists
    ptriangle = {}
    ptriangle[0] = [1]
    ptriangle[1] = [1,1]
    ptriangle[2] = [1,2,1]
    for r in range(3, row_limit):
        ptriangle[r] = []
        for i in range(len(ptriangle[r-1])+1):
            if i == 0: # on left border, so we just add 1
                ptriangle[r].append(1)
            elif i == len(ptriangle[r-1]): # on right border, so we just add 1
                ptriangle[r].append(1)
            else: # not on border, so we sum up the two numbers above
                ptriangle[r].append(ptriangle[r-1][i-1] + ptriangle[r-1][i])

    # Putting all numbers into one list, except the outermost 2 numbers in each row
    number_list = []
    for r in range(row_limit):
        row = ptriangle[r]
        for i, number in enumerate(row):
            if i > 1 and i < len(row)-1: # exclude the outermost 2 numbers in each row
                number_list.append(number)

    # Counting the numbers
    number_set = set(number_list) 
    pascal_multiples = []
    for unique_number in number_set:
        count = 0
        for number in number_list:
            if number == unique_number:
                count = count + 1
        if count > 3:
            pascal_multiples.append(unique_number)
    
    return sorted(pascal_multiples)


from timeit import default_timer as timer

def main():
	row_limit = 250

	start = timer()
	print(search_pascal_multiples_slow(row_limit))
	end = timer()
	runtime_slow = end-start

	start = timer()
	print(search_pascal_multiples_fast(row_limit))
	end = timer()
	runtime_fast = end-start

	print(round(runtime_slow / runtime_fast, 2))

if __name__ == "__main__":
	main()