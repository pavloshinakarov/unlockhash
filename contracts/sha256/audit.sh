cargo clean
cargo build-sbf
solana program dump CJeVWuAWw4XUeoNHD72cTJjGTzxvFdtqZtY3d9Bcik8N dump.so
sha256sum dump.so ./target/deploy/sha256_contract.so
