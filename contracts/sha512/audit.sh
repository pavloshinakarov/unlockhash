cargo clean
cargo build-sbf
solana program dump 51qXu1vgg2VXmUN2GF3XeseCzfpQfMmtCE95cqto9ekZ dump.so
sha256sum dump.so ./target/deploy/sha512_contract.so
