from solana.rpc.api import Client
import base64
import json
import time
from datetime import datetime
from solders.pubkey import Pubkey
import config

def blockchain(algorithm: str, network: str, storage_account: str):
    if network == "mainnet":
        url = config.rpc["mainnet"]
    elif network == "devnet":
        url = config.rpc["devnet"]
    else:
        raise ValueError("Unsupported network")

    client = Client(url)

    claimed_false = {}
    claimed_true = {}

    if storage_account != "0":
        storage_pubkey = Pubkey.from_string(storage_account)
        
        signatures_resp = client.get_signatures_for_address(storage_pubkey, limit=1000)

        signatures = signatures_resp.value

        for sig_info in signatures:
            sig = sig_info.signature
            tx_resp = client.get_transaction(sig, encoding="jsonParsed")
            result = tx_resp.value

            if result is None:
                continue

            logs = result.transaction.meta.log_messages

            hash_val = ""
            salt = ""
            rounds = ""
            text_received = ""
            lamports = 0

            for log in logs:
                if "Hash: " in log:
                    json_bytes = log.split("Hash: ")[1].strip()
                    byte_arr = json.loads(json_bytes)
                    hash_val = ''.join(f'{int(b):02x}' for b in byte_arr)

                if "Salt: " in log:
                    salt = log.split("Salt: ")[1].strip()

                if "Rounds: " in log:
                    rounds = log.split("Rounds: ")[1].strip()

                if "Amount for claim: " in log:
                    lamports = int(log.split("Amount for claim: ")[1])

            # If hash and lamports ... add to claimedFalse
            if hash_val and lamports:
                register = {
                    "hash": hash_val,
                    "reward": lamports / 1e9,
                    "salt": [salt],
                    "rounds": [rounds],
                    "url": f"https://explorer.solana.com/tx/{sig}?cluster={network}"
                }
                claimed_false[hash_val] = register

            # Search hashes claimed (Operation 2)
            for log in logs:
                if algorithm + " Hash Calculated: " in log:
                    hash_val = log.split(algorithm + " Hash Calculated: ")[1].strip()

                if "Text received: " in log and not text_received:
                    text_received = log.split("Text received: ")[1].strip()

                if "Transferring " in log and " lamports" in log:
                    lamports = int(log.split("Transferring ")[1].split(" lamports")[0])

            if hash_val and text_received and lamports:
                register = {
                    "hash": hash_val,
                    "reward": lamports / 1e9,
                    "secret": text_received,
                    "salt": [],
                    "rounds": [],
                    "url": f"https://explorer.solana.com/tx/{sig}?cluster={network}",
                }

                if hash_val in claimed_false:
                    del claimed_false[hash_val]

                claimed_true[hash_val] = register

        time.sleep(0.3)

    with open("dump_" + algorithm.lower() + ".json", "w") as f:
        json.dump(list(claimed_false.values()), f, indent=2)

    #print(f">>> {len(claimed_false)} {algorithm} records saved")


#dump("MD5", "devnet", "9jVkvcKTe378tBycwutcxwqCLJWaFopSSo6K3mQsRMtv")