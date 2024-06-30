"""generates a realistic email address
structure is: 
    sec1 = {name1/word1}
    sec2 = {1number/2numbers/decimal/null/decimal/hyphen/undescore}
    sec3 = {name2/word2/null}
    sec4 = {1number/2numbers/null}
    domain = {weighted choice from list of domains by number of users in millions}
"""

from random import randint, choices
import json
import names

def generate_random_email(email_domains,word_list):
    domains = [item[0] for item in email_domains]
    weights = [item[1] for item in email_domains]

    sel_domain = choices(domains,weights)[0]

    sec1type = choices(["name","word"],[80,20])[0]
    if sec1type == "name":
        sec1 = names.get_first_name().lower()
    else:
        sec1 = choices(word_list)[0]
    sec2type = choices(["1number","2number",".","_","-",""])[0]
    if sec2type == "1number":
        sec2 = randint(0,9)
    elif sec2type == "2number":
        sec2 = randint(10,99)
    else:
        sec2 = sec2type
    sec3type = choices(["name","word",""],[40,10,50])[0]
    if sec3type == "name":
        sec3 = names.get_last_name().lower()
    elif sec3type == "word":
        sec3 = choices(word_list)[0]
    else:
        sec3 = sec3type
    sec4type = choices(["1number","2number",""],[40,10,50])[0]
    if sec4type == "1number":
        sec4 = randint(0,9)
    elif sec4type == "2number":
        sec4 = randint(10,99)
    else:
        sec4 = sec4type

    email = f"{sec1}{sec2}{sec3}{sec4}"
    if not email[-1].isalnum():  # if last character is not alphanumeric
        email = email[:-1]  # remove from end of email
    email = f"{email}@{sel_domain}"

    return email

if __name__ == "__main__":
    # test print 100 generated email addresses
    with open("domains.json") as f:
        email_domains = json.load(f)  # random email domain, weighted by number of users in millions
    with open("words.json") as f:
        word_list = json.load(f)
    for i in range(100):
        print(generate_random_email(email_domains,word_list))