import random
import names
from src.utils.emailHosts import weighted_email_domains

def name_gen():
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    name_system = random.choice(["FullName", "FullFirstFirstInitial", "FirstInitialFullLast"])
    if name_system == "FullName":
        return first_name + last_name
    elif name_system == "FullFirstFirstInitial":
        return first_name + last_name[0]
    return first_name[0] + last_name

def generate_random_email():
    name = name_gen()
    use_number = random.choice([True, False])
    
    cumulative_weights = []
    total_weight = 0
    for domain, weight in weighted_email_domains:
        total_weight += weight
        cumulative_weights.append((domain, total_weight))
    
    random_number = random.randint(1, total_weight)
    for domain, cumulative_weight in cumulative_weights:
        if random_number <= cumulative_weight:
            selected_domain = domain
            break
    
    if use_number:
        return f"{name}{random.randint(1, 100)}{selected_domain}"
    else:
        return f"{name}{selected_domain}"
