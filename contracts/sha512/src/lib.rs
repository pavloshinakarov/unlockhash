use solana_program::{
    account_info::{AccountInfo},
    entrypoint,
    entrypoint::ProgramResult,
    msg,
    pubkey::Pubkey,
    program_error::ProgramError,
    system_instruction,
    program::invoke,
    program::invoke_signed,
    sysvar::Sysvar,
    sysvar::rent::Rent,
    clock::Clock
};

use sha2::{Sha512, Digest};

use std::str::FromStr;

entrypoint!(process_instruction);

const RECORD_SIZE: usize = 113; // hash (64) + amount(8) + claimed (1) + time (8) + sender (32)

fn process_instruction(
    _program_id: &Pubkey,
    accounts: &[AccountInfo],
    instruction_data: &[u8],
) -> ProgramResult {
    msg!("INIT");

    let storage_account = &accounts[0];  // Cuenta de almacenamiento
    let pda_account = &accounts[2];

    if storage_account.owner != _program_id {
        msg!("State account is not owned by the program.");
        return Err(ProgramError::IllegalOwner);
    }

    let seed = "pda_sha512";
    let (derived_pda, _bump_seed) = Pubkey::find_program_address(&[seed.as_bytes()], _program_id);

    if derived_pda != *pda_account.key {
        msg!("Contract account its not the contract account");
        return Err(ProgramError::IncorrectProgramId);
    }

    let operation = instruction_data[0];
    msg!("Operation: {}", operation);
    match operation {
        1 => add_hash(_program_id, accounts, &instruction_data[1..4], &instruction_data[4..]),
        2 => claim_amount(_program_id, accounts, &instruction_data[1..4], &instruction_data[4..]),
        3 => resize(_program_id, accounts),
        4 => refund_amount(_program_id, accounts, &instruction_data[1..]),
        _ => Err(ProgramError::InvalidInstructionData)
    }
}

fn add_hash(_program_id: &Pubkey, accounts: &[AccountInfo], rounds_data: &[u8], data: &[u8]) -> ProgramResult {
    let storage_account = &accounts[0];
    let sender_account = &accounts[1];
    let pda_account = &accounts[2];    
    let system_program = &accounts[3];
    let owner_account = &accounts[4];
    let burn_account = &accounts[5];
    
    let expected_burn_account = Pubkey::from_str("2wpG7omsTYGPDj5qMtnAkV69jWAuRG7uJ7wqCWwu67Kn")
        .expect("Invalid address");
    
    if *burn_account.key != expected_burn_account {
        return Err(ProgramError::Custom(6));
    }

    let expected_owner_account = Pubkey::from_str("4W47DbSDBqdKpWraMeg7wED4ExumuQqwWhsGz14L4UXS")
        .expect("Invalid address");
    
    if *owner_account.key != expected_owner_account {
        return Err(ProgramError::Custom(7));    
    }

    let rounds_bytes = &rounds_data[..3];
    let rounds = u32::from_be_bytes([0, rounds_bytes[0], rounds_bytes[1], rounds_bytes[2]]);
    if rounds > 0 {
        msg!("Rounds: {}", rounds);
    } else {
        msg!("Rounds must be greater than 0");
        return Err(ProgramError::InvalidInstructionData);
    }

    let mut storage_data = storage_account.try_borrow_mut_data()?;

    let previous_balance = u64::from_le_bytes(storage_data[0..8].try_into().unwrap());
    msg!("Previous balance: {}", previous_balance);

    let current_balance = pda_account.lamports();
    msg!("Current balance: {}", current_balance);

    let input_amount = current_balance - previous_balance;
    if input_amount < 1000000 {
        return Err(ProgramError::Custom(4));
    }
    msg!("Amount transferred: {}", input_amount);
    let amount = (input_amount / 100) * 70;
    msg!("Amount for claim: {}", amount);
    let amount_burn = (input_amount / 100) * 20;
    let amount_team = (input_amount / 100) * 10;
    msg!("Amount for burn: {}", amount_burn);
    msg!("Amount for team: {}", amount_team);

    let current_balance_without_burn_and_team = current_balance - amount_burn - amount_team;
    storage_data[0..8].copy_from_slice(&current_balance_without_burn_and_team.to_le_bytes());

    if data.len() < 1 {
        return Err(ProgramError::InvalidInstructionData); // Hash (64) + amount (8)
    }

    const NULL_HASH: [u8; 64] = [0; 64];
    let hash = &data[..64];

    if hash == NULL_HASH {
        msg!("Hash null");
        return Err(ProgramError::Custom(5));
    }
    msg!("Hash: {:?}", hash);
    
    let storage_data_ff = &mut storage_data[8..]; //skip balance storage area

    let mut create = true;

    for record in storage_data_ff.chunks_exact_mut(RECORD_SIZE) {
        if record[..64] == hash[..] {
            create = false;
            msg!("Hash already exists");
            if record[72] == 0 {
                let expected_sender_account = Pubkey::new_from_array(record[81..113].try_into().unwrap());
                if *sender_account.key != expected_sender_account {
                    msg!("Only same owner can update claim amount.");
                    return Err(ProgramError::Custom(9));    
                }
                let old_amount = u64::from_le_bytes(record[64..72].try_into().unwrap());
                let new_amount = old_amount + amount;
                record[64..72].copy_from_slice(&new_amount.to_le_bytes());
                let current_play = Clock::get().map_err(|_| ProgramError::InvalidAccountData)?.unix_timestamp;
                record[73..81].copy_from_slice(&current_play.to_le_bytes());
                msg!("Hash updated successfully.");             
            }else{
                msg!("This hash has already been claimed.");
                return Err(ProgramError::Custom(1));
            }

        }
    }

    let salt_length = data[64];
    msg!("Salt length: {}", salt_length);

    let salt_text = String::from_utf8_lossy(&data[65..65 + salt_length as usize]);    
    msg!("Salt: {}", salt_text);

    let transfer_instruction_burn = system_instruction::transfer(
        &pda_account.key,
        &burn_account.key,
        amount_burn,
    );

    let seed = b"pda_sha512";
    let (pda, bump) = Pubkey::find_program_address(&[seed], &_program_id);
    println!("PDA: {}, Bump: {}", pda, bump);
    let seeds = &[b"pda_sha512".as_ref(), &[bump]];

    invoke_signed(
        &transfer_instruction_burn,
        &[pda_account.clone(), burn_account.clone(), system_program.clone()],
        &[seeds],
    )?;

    let transfer_instruction_team = system_instruction::transfer(
        &pda_account.key,
        &owner_account.key,
        amount_team,
    );

    let seed = b"pda_sha512";
    let (pda, bump) = Pubkey::find_program_address(&[seed], &_program_id);
    println!("PDA: {}, Bump: {}", pda, bump);
    let seeds = &[b"pda_sha512".as_ref(), &[bump]];

    invoke_signed(
        &transfer_instruction_team,
        &[pda_account.clone(), owner_account.clone(), system_program.clone()],
        &[seeds],
    )?;    

    if create == true{
        for record in storage_data_ff.chunks_exact_mut(RECORD_SIZE) {
            if record[64..].iter().all(|&x| x == 0) {
                record[..64].copy_from_slice(hash);
                record[64..72].copy_from_slice(&amount.to_le_bytes());
                record[72] = 0; // `claimed` en false
                let current_play = Clock::get().map_err(|_| ProgramError::InvalidAccountData)?.unix_timestamp;                                
                record[73..81].copy_from_slice(&current_play.to_le_bytes());
                record[81..113].copy_from_slice(sender_account.key.as_ref()); 
                msg!("Hash added successfully.");
                return Ok(());
            }
        }

        msg!("No space left.");

        return Err(ProgramError::Custom(8));    
    }

    return Ok(());
}

fn claim_amount(
    _program_id: &Pubkey, 
    accounts: &[AccountInfo],
    rounds_data: &[u8], 
    data: &[u8]
) -> ProgramResult {
    let storage_account = &accounts[0];
    let sender_account = &accounts[1];
    let pda_account = &accounts[2];
    let system_program = &accounts[3];

    let storage_data = storage_account.try_borrow_mut_data()?;

    if data.len() < 1 {
        return Err(ProgramError::InvalidInstructionData);
    }

    let rounds_bytes = &rounds_data[..3];
    let rounds = u32::from_be_bytes([0, rounds_bytes[0], rounds_bytes[1], rounds_bytes[2]]);
    if rounds > 0 {
        msg!("Rounds: {}", rounds);
    } else {
        msg!("Rounds must be greater than 0");
        return Err(ProgramError::InvalidInstructionData);
    }

    let input_text = String::from_utf8_lossy(data);
    msg!("Text received: {}", input_text);

    let mut hasher = Sha512::new();
    hasher.update(input_text.as_ref());
    let mut hash = hasher.finalize();
    let mut hash_print = hex::encode(hash);
    msg!("SHA-512 Hash Calculated: {}", hash_print);

    for _ in 1..rounds {
        hasher = Sha512::new();
        msg!("Text received: {}", hash_print);
        hasher.update(hash_print);
        hash = hasher.finalize();
        hash_print = hex::encode(hash);
        msg!("SHA-512 Hash Calculated: {}", hash_print);
    }

    let mut record_index = None;
    let mut amount = 0;

    let storage_data_ff = &storage_data[8..];

    for (i, record) in storage_data_ff.chunks_exact(RECORD_SIZE).enumerate() {
        if record[..64] == hash[..64] {
            if record[72] == 1 {
                msg!("This hash has already been claimed.");
                return Err(ProgramError::Custom(2));
            }

            amount = u64::from_le_bytes(record[64..72].try_into().unwrap());
            record_index = Some(i);
            break;
        }
    }

    let record_index = record_index.ok_or_else(|| {
        msg!("Hash not found.");
        ProgramError::Custom(3)
    })?;

    drop(storage_data);

    msg!("Transferring {} lamports to the calling account...", amount);

    let transfer_instruction = system_instruction::transfer(
        &pda_account.key,
        &sender_account.key,
        amount,
    );

    let seed = b"pda_sha512";
    let (pda, bump) = Pubkey::find_program_address(&[seed], &_program_id);
    println!("PDA: {}, Bump: {}", pda, bump);
    let seeds = &[b"pda_sha512".as_ref(), &[bump]];

    invoke_signed(
        &transfer_instruction,
        &[pda_account.clone(), sender_account.clone(), system_program.clone()],
        &[seeds],
    )?;

    msg!("Transfer completed successfully.");

    let mut storage_data = storage_account.try_borrow_mut_data()?;

    let current_balance = u64::from_le_bytes(storage_data[0..8].try_into().unwrap());
    msg!("Current balance: {}", current_balance);    

    msg!("Transfer Amount: {}", amount);

    let new_amount = current_balance - amount;
    msg!("New Amount: {}", new_amount);

    storage_data[0..8].copy_from_slice(&new_amount.to_le_bytes());
   
    let start = 8 + (record_index * RECORD_SIZE);
    let end = start + RECORD_SIZE;
    let record = &mut storage_data[start..end];
    record[72] = 1;

    Ok(())
}


fn resize(_program_id: &Pubkey, accounts: &[AccountInfo]) -> ProgramResult {
    let storage_account = &accounts[0];
    let sender_account = &accounts[1];
    //let pda_account = &accounts[2];    
    let system_program = &accounts[3];

    let new_size = storage_account.data.borrow().len() + (RECORD_SIZE * 10);

    let rent = Rent::get()?;
    let new_minimum_balance = rent.minimum_balance(new_size);

    let lamports_diff = new_minimum_balance.saturating_sub(storage_account.lamports());
    invoke(
      &system_instruction::transfer(sender_account.key, storage_account.key, lamports_diff),
      &[
          sender_account.clone(),
          storage_account.clone(),
          system_program.clone(),
      ],
    )?;

    storage_account.realloc(new_size, false)?;

    Ok(())
}

fn refund_amount(
    _program_id: &Pubkey, 
    accounts: &[AccountInfo],
    data: &[u8]
) -> ProgramResult {
    let storage_account = &accounts[0];
    let sender_account = &accounts[1];
    let pda_account = &accounts[2];
    let system_program = &accounts[3];

    let storage_data = storage_account.try_borrow_mut_data()?;

    if data.len() < 1 {
        return Err(ProgramError::InvalidInstructionData);
    }

    const NULL_HASH: [u8; 64] = [0; 64];
    let hash = &data[..64];

    if hash == NULL_HASH {
        msg!("Hash null");
        return Err(ProgramError::Custom(10));
    }
    msg!("Hash: {:?}", hash);

    let mut record_index = None;
    let mut amount = 0;

    let storage_data_ff = &storage_data[8..];
    let mut expected_sender_account = Pubkey::default(); 
    
    for (i, record) in storage_data_ff.chunks_exact(RECORD_SIZE).enumerate() {
        if record[..64] == hash[..64] {
            if record[72] == 1 {
                msg!("This hash has already been claimed.");
                return Err(ProgramError::Custom(11));
            }

            let timelapse: i64 = 7 * 24 * 60 * 60; // 1 week
            let current_day = Clock::get().map_err(|_| ProgramError::InvalidAccountData)?.unix_timestamp;
            let sended_day = u64::from_le_bytes(record[73..81].try_into().unwrap());
            msg!("previous date: {:?}, current date: {:?})", sended_day, current_day);
            if (sended_day as i64) + timelapse > current_day {
                msg!("It hasn't even been a week yet.");
                return Err(ProgramError::Custom(12));
            }

            amount = u64::from_le_bytes(record[64..72].try_into().unwrap());
            expected_sender_account = Pubkey::new_from_array(record[81..113].try_into().unwrap());
            record_index = Some(i);
            break;
        }
    }

    let record_index = record_index.ok_or_else(|| {
        msg!("Hash not found.");
        ProgramError::Custom(3)
    })?;

    
    if *sender_account.key != expected_sender_account {
        msg!("Only same owner can refund claim amount.");
        return Err(ProgramError::Custom(9));    
    }

    drop(storage_data);

    msg!("Transferring {} lamports to the calling account...", amount);

    let transfer_instruction = system_instruction::transfer(
        &pda_account.key,
        &sender_account.key,
        amount,
    );

    let seed = b"pda_sha512";
    let (pda, bump) = Pubkey::find_program_address(&[seed], &_program_id);
    println!("PDA: {}, Bump: {}", pda, bump);
    let seeds = &[b"pda_sha512".as_ref(), &[bump]];

    invoke_signed(
        &transfer_instruction,
        &[pda_account.clone(), sender_account.clone(), system_program.clone()],
        &[seeds],
    )?;

    msg!("Transfer completed successfully.");

    let mut storage_data = storage_account.try_borrow_mut_data()?;

    let current_balance = u64::from_le_bytes(storage_data[0..8].try_into().unwrap());
    msg!("Current balance: {}", current_balance);    

    msg!("Transfer Amount: {}", amount);

    let new_amount = current_balance - amount;
    msg!("New Amount: {}", new_amount);

    storage_data[0..8].copy_from_slice(&new_amount.to_le_bytes());
   
    let start = 8 + (record_index * RECORD_SIZE);
    let end = start + RECORD_SIZE;
    let record = &mut storage_data[start..end];

    record[..65].fill(0);

    Ok(())
}