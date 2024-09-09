use num_bigint::BigUint;
use std::str::FromStr;
pub mod prover;
pub mod utils;
pub mod verifier;
use num_traits::cast::ToPrimitive;
use prover::*;
use std::fs::{self, File};
use std::io::{BufWriter, Write};
use utils::*;
use verifier::Verifier;

fn main() -> std::io::Result<()> {
    let flag = b"KMACTF{*******************************************}";
    let num_flag = bytes_to_biguint(flag);

    let num_rounds = num_flag.bits() as usize;

    // Define the folder name
    let folder_name = "Log";

    // Create the folder if it doesn't exist
    if fs::metadata(folder_name).is_err() {
        fs::create_dir(folder_name)?;
    }

    println!("Number of rounds: {}", num_rounds);

    let x = BigUint::from_str(
        "106276637345585586395178695555113419125706596151484787339368729136766801222943",
    )
    .unwrap();
    let y = BigUint::from_str(
        "67502870359608496464376733754660348616157530226832182619029429292243849029379",
    )
    .unwrap();

    let prover = Prover::new(x.clone(), y.clone(), num_rounds);
    let mut verifier = Verifier::new(x.clone(), y.clone(), num_rounds);

    for i in 0..num_rounds {
        let file_name = format!("{}/output_{}.txt", folder_name, i);
        let file = File::create(&file_name)?;

        let mut writer = BufWriter::new(file);

        writeln!(writer, "Round {}", i)?;

        let bit = ((&num_flag >> i) & BigUint::from(1_u32))
            .to_u32()
            .expect("Can not do this");

        let r = verifier.get_r();

        // give the prover the pair and r
        let w = verifier.gen_w(bit as i32, &r);
        let pair = verifier.gen_pairs();

        writeln!(writer, "w = {}", w)?;

        writeln!(writer, "Pair = ")?;
        for p in pair {
            writeln!(writer, "({}, {})", p.0, p.1)?;
        }

        let list_i = prover.gen_list_i();
        writeln!(writer, "list_i = {:?}", list_i)?;

        let v = verifier.respond(&bit, list_i, &r);

        let v = convert_rp_to_string(&v);

        writeln!(writer, "list_of_respond = ")?;
        for line in v {
            writeln!(writer, "{}", line)?;
        }

        writer.flush()?;
    }

    Ok(())
}
