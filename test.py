# A simple generator function
def my_gen_1():
    n = 1
    # print('This is printed first')
    # Generator function contains yield statements
    yield n

    n += 1
    # print('This is printed second')
    yield n
    return
    n += 1
    # print('This is printed at last')
    yield n

def my_gen():
    return my_gen_1()

# Using for loop
iterator = my_gen()
print(next(iterator))
# print(next(iterator))
# print(next(iterator))
for item in iterator:
    print("#" + str(item))    