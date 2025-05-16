import os
import time
import random
from colorama import init, Fore, Style
from pyfiglet import Figlet
import config
import hashcat
import dump
import json
import db
import requests
import os
from io import BytesIO
from datetime import datetime

init(autoreset=True)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_out(text, color=Fore.GREEN, delay=0.02):
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print()

def animated_title(text):
    clear_console()
    type_out(f"Initializing {text} ...", Fore.GREEN, 0.05)
    time.sleep(1)
    clear_console()

def draw_static_title():
    figlet = Figlet(font='slant')
    print(Fore.GREEN + figlet.renderText("Unlockhash"))

def fixed_screen_layout(head_log, body_log):
    width = 80
    draw_static_title()
    print("=" * width)
    print(Fore.GREEN + " LOG ".ljust(60) + Fore.CYAN + "MONITOR".rjust(20))
    print("=" * width)
    for i in range(len(head_log)):
        type_out(head_log[i], Fore.CYAN, 0)
    print("=" * width)
    for i in range(len(body_log)):
        type_out(body_log[i]['text'], body_log[i]['color'], body_log[i]['delay'])
    #print("=" * width)



def fetch_and_display_hashes():
    text = "Unlockhash v0.1"
    animated_title(text)

    head_log = []
    body_log = []

    body_log.append({"text": f"Testing hashcat", "color": Fore.GREEN, "delay": 0.01})
    clear_console()
    fixed_screen_layout(head_log, body_log)

    testHashcat = hashcat.crack("MD5", "0ad066a5d29f3f2a2a1c7c17dd082a79", '"hola mundo"', None)
    if testHashcat[0]['password'] == "hola mundo":
        body_log.append({"text": f"Hashcat working", "color": Fore.CYAN, "delay": 0.01})
        clear_console()
        fixed_screen_layout(head_log, body_log)
        time.sleep(1) 
    else:
        body_log.append({"text": f"Hashcat not working", "color": Fore.RED, "delay": 0})
        
        body_log.append({"text": f"AMD GPUs on Linux require \"AMDGPU\" (21.50 or later) and \"ROCm\" (5.0 or later)", "color": Fore.RED, "delay": 0})
        body_log.append({"text": f"AMD GPUs on Windows require \"AMD Adrenalin Edition\" (Adrenalin 22.5.1 exactly)", "color": Fore.RED, "delay": 0})
        body_log.append({"text": f"Intel CPUs require \"OpenCL Runtime for Intel Core and Intel Xeon Processors\" (16.1.1 or later)", "color": Fore.RED, "delay": 0})
        body_log.append({"text": f"NVIDIA GPUs require \"NVIDIA Driver\" (440.64 or later) and \"CUDA Toolkit\" (9.0 or later)", "color": Fore.RED, "delay": 0})

        clear_console()
        fixed_screen_layout(head_log, body_log)
        exit()

    #LOOP FROM HERE
    attacks = 0
    while True:
        timestamp = int(time.time())
        if config.last_network_dump < timestamp - 60*60:
            config.update_config_key('last_network_dump', timestamp)
            body_log = []
            body_log.append({"text": "Syncing with blockchain", "color": Fore.GREEN, "delay": 0})
            body_log.append({"text": ">>> Obtaining data from the MD5 smart contract...", "color": Fore.CYAN, "delay": 0.01})
            clear_console()
            fixed_screen_layout(head_log, body_log)    
            dump.blockchain(
                algorithm="MD5",
                network="devnet",
                storage_account="9jVkvcKTe378tBycwutcxwqCLJWaFopSSo6K3mQsRMtv"
            )

            body_log[1] = {"text": ">>> Obtaining data from the MYSQL323 smart contract...", "color": Fore.CYAN, "delay": 0.01}
            clear_console()
            fixed_screen_layout(head_log, body_log)
            dump.blockchain(
                algorithm="MySQL",
                network="devnet",
                storage_account="3xTqVtDLVx58h5nPaUesf8zcUHHXpyX87j1dfZAktMR7"
            )
            
            body_log[1] = {"text": ">>> Obtaining data from the NTLM smart contract...", "color": Fore.CYAN, "delay": 0.01}
            clear_console()
            fixed_screen_layout(head_log, body_log)    
            dump.blockchain(
                algorithm="NTLM",
                network="devnet",
                storage_account="4Eyg7QYVQm4JWAvfh3DcsxCntExv4Q3NoX32vovAP7WV"
            )

            body_log[1] = {"text": ">>> Obtaining data from the SHA-1 smart contract...", "color": Fore.CYAN, "delay": 0.01}
            clear_console()
            fixed_screen_layout(head_log, body_log)    
            dump.blockchain(
                algorithm="SHA-1",
                network="devnet",
                storage_account="GGQN4JqAM3F4sxqDZnUZ1jBTFKX1PB66QsLQZK54rjTS"
            )

            body_log[1] = {"text": ">>> Obtaining data from the SHA-256 smart contract...", "color": Fore.CYAN, "delay": 0.01} 
            clear_console()
            fixed_screen_layout(head_log, body_log)
            dump.blockchain(
                algorithm="SHA-256",
                network="devnet",
                storage_account="4GRXLiGAcR9mccguE5Jxb4tmFmPMj6W5kjV3fKQ1SVDr"
            )

            body_log[1] = {"text": ">>> Obtaining data from the SHA-512 smart contract...", "color": Fore.CYAN, "delay": 0.01} 
            clear_console()
            fixed_screen_layout(head_log, body_log)
            dump.blockchain(
                algorithm="SHA-512",
                network="devnet",
                storage_account="55CBW7DhqNV3cGnFxSKGCsrJ8Fj71SisTmaPhd9HzXmK"
            )

        with open("dump_md5.json", "r") as f:
            data_md5 = json.load(f)
            for item in data_md5:
                item["algorithm"] = "MD5"

        with open("dump_mysql.json", "r") as f:
            data_mysql = json.load(f)
            for item in data_mysql:
                item["algorithm"] = "MYSQL323"

        with open("dump_ntlm.json", "r") as f:
            data_ntlm = json.load(f)
            for item in data_ntlm:
                item["algorithm"] = "NTLM"

        with open("dump_sha-1.json", "r") as f:
            data_sha1 = json.load(f)
            for item in data_sha1:
                item["algorithm"] = "SHA-1"

        with open("dump_sha-256.json", "r") as f:
            data_sha256 = json.load(f)
            for item in data_sha256:
                item["algorithm"] = "SHA-256"

        with open("dump_sha-512.json", "r") as f:
            data_sha512 = json.load(f)
            for item in data_sha512:
                item["algorithm"] = "SHA-512"

        data = data_md5 + data_mysql + data_ntlm + data_sha1 + data_sha256 + data_sha512

        summary = {}
        for item in data:
            algo = item["algorithm"]
            summary.setdefault(algo, {"count": 0, "reward": 0, "items": []})
            summary[algo]["count"] += 1
            summary[algo]["reward"] += item["reward"]
            summary[algo]["items"].append(item)

        head_log = []
        head_log.append(f"Attacks: {attacks}")
        head_log.append(f"Passwords: {db.get_all_passwords()}")

        dt = datetime.fromtimestamp(config.last_network_dump)
        last_network_dump_formatted = dt.strftime("%d/%m/%Y %H:%M")
        head_log.append(f"Blockchain synchronized {last_network_dump_formatted}")
        for algo, stats in summary.items():
            head_log.append(f"  [{algo}] Hashes: {stats['count']}  -  Total Reward: {round(stats['reward'], 2):.2f} SOL")

        clear_console()
        fixed_screen_layout(head_log, body_log)

        algorithms = []
        if len(data_md5) > 0:
            algorithms.append("MD5")
        if len(data_mysql) > 0:
            algorithms.append("MYSQL323")
        if len(data_ntlm) > 0:
            algorithms.append("NTLM")
        if len(data_sha1) > 0:
            algorithms.append("SHA-1")
        if len(data_sha256) > 0:
            algorithms.append("SHA-256")
        if len(data_sha512) > 0:
            algorithms.append("SHA-512")

        body_log = []

        algorithm = random.choice(algorithms)
        item = random.choice(summary[algorithm]["items"])
        
        random_mask = hashcat.generate_random_mask()

        while db.exists(random_mask["mask"], item["hash"], item["algorithm"]):
            random_mask = hashcat.generate_random_mask()

        estimated_duration = db.estimated_time(config.author, algorithm, config.max_complexity)

        if estimated_duration < 60:
            estimated_time_string = f"{estimated_duration:.0f} seconds"
        else:
            estimated_time_string = f"{(estimated_duration / 60):.1f} minutes"

        if estimated_duration == 0:
            head_log.append(f"Estimated time for max complexity {algorithm} will be calculated next time")
        else:
            head_log.append(f"Estimated time for max complexity {algorithm}: {estimated_time_string}")

        random_mask_estimated_time = estimated_duration * (random_mask["complexity"] / config.max_complexity)

        body_log.append({"text": f"Target: Algorithm = {algorithm}", "color": Fore.GREEN, "delay": 0})
        body_log.append({"text": f"Hash = {item['hash']}", "color": Fore.GREEN, "delay": 0})
        body_log.append({"text": f"Random mask = {random_mask['mask']}", "color": Fore.GREEN, "delay": 0})
        body_log.append({"text": f"Complexity = {random_mask['complexity']}", "color": Fore.GREEN, "delay": 0})
        if estimated_duration == 0:
            body_log.append({"text": f"Estimated time will be calculated next time", "color": Fore.CYAN, "delay": 0})
        else:
            if random_mask_estimated_time < 60:
                random_mask_estimated_time_string = f"{random_mask_estimated_time:.0f} seconds"
            else:
                random_mask_estimated_time_string = f"{(random_mask_estimated_time / 60):.1f} minutes"
            body_log.append({"text": f"Estimated time: {random_mask_estimated_time_string} (could vary)", "color": Fore.CYAN, "delay": 0})
        
        dt = datetime.fromtimestamp(timestamp)
        hashcat_start_time_formatted = dt.strftime("%d/%m/%Y %H:%M")
        body_log.append({"text": f"Hashcat start working at {hashcat_start_time_formatted}", "color": Fore.GREEN, "delay": 0})

        clear_console()
        fixed_screen_layout(head_log, body_log)

        other_hashs = []
        for i in summary[algorithm]["items"]:
            if i["salt"][0] == item["salt"][0]:
                if i["rounds"][0] == item["rounds"][0]:
                    if i["rounds"][0] == 1: # rounds > 1; NOT SUPPORTED YET by hashcat for md5, sha-1 etc.
                        other_hashs.append(i["hash"])

        # salt is dangerous for hashcat command line; NOT SUPPORTED YET
        #if item["salt"][0]:
        #    random_mask = item["salt"].replace('$password', random_mask)

        start = time.time()
        passwords = hashcat.crack(item["algorithm"], item["hash"], random_mask["mask"], other_hashs)
        end = time.time()
        duration = end - start

        for op in passwords:
            db.store(random_mask["mask"], op['hash'], item["algorithm"], config.author, op['password'], random_mask["complexity"], duration)

        attacks = attacks + 1

fetch_and_display_hashes()
