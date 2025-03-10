cargo clean
cargo build-sbf
solana program dump DNbRGxK74P8GxQD6EcSG6VV5gKQ6W2SWQUyUkzMnGkZr dump.so
sha256sum dump.so ./target/deploy/sha1_contract.so
