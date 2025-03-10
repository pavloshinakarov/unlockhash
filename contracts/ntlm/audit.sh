cargo clean
cargo build-sbf
solana program dump 59zjEunuZsY3KNehZVQRaCPHmKozeK7G81Wv84T8fW79 dump.so
sha256sum dump.so ./target/deploy/ntlm_contract.so
