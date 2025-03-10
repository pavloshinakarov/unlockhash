cargo clean
cargo build-sbf
solana program dump 3GMeUamudZMwMYTMVuaVXmVAn2EcwFBccJT26NX46MZ3 dump.so
sha256sum dump.so ./target/deploy/md5_contract.so
