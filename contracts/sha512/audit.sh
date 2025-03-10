cargo clean
cargo build-sbf
solana program dump 9QEcLhGBdcjxQsUg9W5EsmKQTaYnmCRAarUTJQC8Sqyx dump.so
sha256sum dump.so ./target/deploy/sha512_contract.so
