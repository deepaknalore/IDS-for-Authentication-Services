import string
import random

ALLOWED_CHARACTERS = string.ascii_letters + string.digits + string.punctuation + ' '

def insert_one_char(word):
    """insert 1 character in the word at some location. Returns a list of
    modifications of @word
    """
    return [word[:i]+c+word[i:]
            for i in range(len(word))
            for c in ALLOWED_CHARACTERS]

def delete_one_char(word):
    """
    deletes one of the characters in the word.
    """
    return [word[:i]+word[i+1:]
            for i in range(len(word))]

def passwordTypo(word):
    if(random.choices([0, 1], [0.5, 0.5])[0]):
        typos =  insert_one_char(word)
    else:
        typos = delete_one_char(word)
    return random.choice(typos)

if __name__ == "__main__":
    print(passwordTypo("password"))
