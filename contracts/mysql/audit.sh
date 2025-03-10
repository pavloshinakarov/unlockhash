cargo clean
cargo build-sbf
solana program dump CnAeUEDCHnAeGgfXiJk3tWHnyLREJFJmGgeSiWA49Xfc dump.so
sha256sum dump.so ./target/deploy/mysql_contract.so
