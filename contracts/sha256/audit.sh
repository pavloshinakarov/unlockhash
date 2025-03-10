cargo clean
cargo build-sbf
solana program dump BiSuPoXimQfHpQzdk3hREB6qPzCXPMKdCfLweCkYQbwk dump.so
sha256sum dump.so ./target/deploy/sha256_contract.so
