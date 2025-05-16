import os
import subprocess
import config
import random
from colorama import init, Fore, Style
import psutil

def is_hashcat_running():
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            name = proc.info.get('name', '') or ''
            cmdline = proc.info.get('cmdline') or []

            if 'hashcat' in name.lower() or any('hashcat' in arg.lower() for arg in cmdline):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

def kill_hashcat_processes():
    killed = 0
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            name = proc.info.get('name', '') or ''
            cmdline = proc.info.get('cmdline') or []

            if 'hashcat' in name.lower() or any('hashcat' in arg.lower() for arg in cmdline):
                proc.kill()
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return killed

def crack(algorithm, hash, mask, other_hashs):

    if os.name == "posix":
        hashcat_hash = "hashcat/hash.txt"
    if os.name == "nt":
        hashcat_hash = "hashcat\\hash.txt"

    hashs = []
    with open(hashcat_hash, 'w') as f:
        f.write(hash + '\n')
        hashs.append({'hash': hash, 'password': False})

        if other_hashs:
            for oh in other_hashs:
                f.write(oh + '\n')
                hashs.append({'hash': oh, 'password': False})

    hashcat_binary = ""
    if os.name == "posix":
        hashcat_binary = "./hashcat.bin"
    if os.name == "nt":
        hashcat_binary = "hashcat.exe"

    hash_mode = config.hash_modes[algorithm.upper()]

    hashcat_command = f"{hashcat_binary} -a 3 -m {hash_mode} hash.txt {mask} --potfile-disable --restore-disable -O"
    print(Fore.MAGENTA + hashcat_command)
    os.chdir("hashcat")

    if is_hashcat_running():
        print(Fore.RED + "Hashcat is already running. Killing ...")
        kill_hashcat_processes()

    output = subprocess.run(hashcat_command, shell=True, text=True, capture_output=True)
    
    os.chdir("..")
    output_lines = output.stdout.splitlines()
    
    response = []
    for line in output_lines:
        for h in range(len(hashs)):
            searchPassword = line.strip().replace(hashs[h]['hash'] + ':', '')
            if searchPassword != line.strip():
                hashs[h]['password'] = searchPassword

    return hashs

mask_complexity = {
    '?l': 26,
    '?u': 26,
    '?d': 10,
    '?s': 33,
    '?a': 95
}

#full_literals = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
literals = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$*")

mask_elements = list(mask_complexity.keys()) + literals

def estimate_mask_complexity(mask: list) -> int:
    total = 1
    for token in mask:
        if token in mask_complexity:
            total *= mask_complexity[token]
        else:
            total *= 1
    return total

def generate_random_mask():
    dynamic_tokens = list(mask_complexity.keys())

    while True:
        length = random.randint(6, 20)

        for _ in range(100):
            num_dynamic = random.randint(1, 12)
            base_mask = [random.choice(dynamic_tokens) for _ in range(num_dynamic)]
            complexity = estimate_mask_complexity(base_mask)
            if config.min_complexity <= complexity <= config.max_complexity:
                remaining = length - num_dynamic
                full_mask = base_mask + random.choices(literals, k=remaining)
                random.shuffle(full_mask)
                return {
                    'mask': ''.join(full_mask),
                    'complexity': complexity
                }

#print(estimate_mask_complexity(['?d','?d','?d','?d','?d','?d','?d','?d','?d','?d', '?d', '?d']))