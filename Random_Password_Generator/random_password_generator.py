from random import choice

len_of_password=12
valid_chars_for_password="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-~?"

password=[]

random_pass="".join(choice(valid_chars_for_password) for each_char in range(len_of_password))
print random_pass