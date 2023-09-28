import array
import random
import secrets
import string


def gen_session(length: int):
    return secrets.token_urlsafe(length)


def gen_verification_code(length: int):
    letters = string.digits
    return "".join(random.choice(letters) for i in range(length))


def gen_password():
    pwd_length = random.randint(8, 16)

    invalid_chars = [">", "<"]
    lower_letters = [i for i in string.ascii_lowercase]
    upper_letters = [i for i in string.ascii_uppercase]
    digits = [i for i in string.digits]
    special_chars = [i for i in string.punctuation if i not in invalid_chars]

    rand_digit = random.choice(digits)
    rand_upper = random.choice(upper_letters)
    rand_lower = random.choice(lower_letters)
    rand_symbol = random.choice(special_chars)

    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol

    all_chars = lower_letters + upper_letters + digits + special_chars

    temp_pass_list = []
    for x in range(pwd_length - 4):
        temp_pass = temp_pass + random.choice(all_chars)
        temp_pass_list = array.array("u", temp_pass)
        random.shuffle(temp_pass_list)

    return "".join(temp_pass_list)
