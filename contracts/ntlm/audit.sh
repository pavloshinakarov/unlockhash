cargo clean
cargo build-sbf
solana program dump HKNaw36nB4cTjqHr74VWJKmp6VgerqgBUbhXKnojZ2FW dump.so
sha256sum dump.so ./target/deploy/ntlm_contract.so
