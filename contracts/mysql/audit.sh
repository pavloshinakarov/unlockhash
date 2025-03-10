cargo clean
cargo build-sbf
solana program dump 3pmNw5i29jm3siHMeBPrepzuimf275DGwWYwVaAJLbh4 dump.so
sha256sum dump.so ./target/deploy/mysql_contract.so
