cargo clean
cargo build-sbf
solana program dump F3d2JyP3cBxHememgZ7ynavWuMVcKZSKCbFSCQc31KXv dump.so
sha256sum dump.so ./target/deploy/sha1_contract.so
