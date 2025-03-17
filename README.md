# UnlockHash - Revolutionizing Cybersecurity with Blockchain

[Unlockhash](https://unlockhash.com) is a cutting-edge platform leveraging blockchain technology to enhance the transparency, security, and rewards of hash cracking tasks. Unlike unreliable platforms, our system guarantees secure processes and equitable rewards through the use of smart contracts. 

Experts can confidently test hash strength, free from intermediaries, with a focus on innovation and transparency. Have fun cracking passwords and earn money!

## 🚀 About the Project

Unlockhash introduces a decentralized way to crack hashes, rewarding participants with the Solana-based **Unlockhash Token** (UNH). This platform uses **smart contracts** deployed on **Solana** to ensure a fully decentralized and transparent environment.

## 🔐 Hash Algorithms Supported

The project currently supports the following hash algorithms, with smart contracts deployed for each:

- **MD5**
- **SHA-1**
- **SHA-256**
- **SHA-512**
- **MySQL**
- **NTLM**

These contracts are available in the `contracts/` folder, and are ready to be audited by the community.

## 🌐 How It Works

The process is divided into two key stages:

### Stage 1: Submit Hash and Reward

1. A user who wants to crack a hash submits the hash (e.g., MD5) and specifies a reward in Solana (SOL).
   
2. **If the hash has already been cracked**, the result will appear in the "Cracked Hashes" list, allowing the user to access the solution without paying.

3. **If there is an active search** for the same hash, the rewards accumulate and are shared among the participants attempting to crack it.

### Stage 2: Claim Attempt

1. Once a user successfully cracks the hash and uploads the result, the system automatically verifies its correctness.

2. **Upon validation**, the reward is released to the person who cracked the hash.

### Transparency

- All cracked hashes will be publicly listed in the **Claimed Hashes** section.
- **MD5** is an example algorithm, but **future integrations** will include additional hash algorithms such as **SHA3** and others.

### Solana Reward Distribution

The reward distribution for each cracked hash is as follows:

- **70%** of the reward goes to the user who cracked the hash.
- **20%** of the reward is used to purchase and burn Unlockhash tokens.
- **10%** of the reward is reserved for the Unlockhash team.

### Fully Decentralized

The entire platform operates under a **DeFi (Decentralized Finance)** model, ensuring full transparency and fairness. The source code is open and available for public auditing, empowering users and experts to verify the platform's integrity.

## 🛠️ Smart Contracts

The core of Unlockhash is powered by smart contracts on **Solana**. These contracts govern the submission and claiming process for hash cracking. They are available in the `contracts/` directory of this repository. The contracts are written for each algorithm:

- [MD5](https://github.com/pavloshinakarov/unlockhash/tree/gh-pages/contracts/md5)
- [SHA-1](https://github.com/pavloshinakarov/unlockhash/tree/gh-pages/contracts/sha1)
- [SHA-256](https://github.com/pavloshinakarov/unlockhash/tree/gh-pages/contracts/sha256)
- [SHA-512](https://github.com/pavloshinakarov/unlockhash/tree/gh-pages/contracts/sha512)
- [MySQL](https://github.com/pavloshinakarov/unlockhash/tree/gh-pages/contracts/mysql)
- [NTLM](https://github.com/pavloshinakarov/unlockhash/tree/gh-pages/contracts/ntlm)

These contracts are ready for review and audit.

## 🏗️ Getting Started

### Prerequisites

- [Solana CLI](https://docs.solana.com/cli/install-solana-cli-tools) installed on your machine.
- A Solana wallet with some SOL for deployment.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/unlockhash.git
   ```

2. Navigate to the contracts/ directory:

   ```bash
   cd unlockhash/contracts
   ```

3. Deploy the smart contracts using Solana tools. You may refer to the Solana documentation for details on deployment. There is an audit.sh where the simplified steps are.

### Contract Auditing

All the contracts are publicly available in this repository, ensuring complete transparency. Anyone can audit the source code to verify the logic and ensure the integrity of the platform.

### 🔧 Future Improvements

1. **Additional Hash Algorithms:** Future versions will include new hashing algorithms like SHA3 and others.
2. **Enhanced Rewards System:** Exploring ways to further improve reward distributions and tokenomics.
3. **User Interface Updates:** Continued improvements to the UI/UX for better user experience.

### 🤝 Contributing

We welcome contributions to improve Unlockhash. If you want to contribute to the project, feel free to submit a pull request or open an issue.
📜 License

Distributed under the MIT License. See LICENSE for more information.

Feel free to visit us at Unlockhash.com.

### 🌐 **Connect With Us**
- [Site](https://unlockhash.com)
- [Twitter](https://x.com/unlockhash)
- [Telegram](https://t.me/Unlockhashproject)
- [Instagram](https://www.instagram.com/unlockhash)
    
