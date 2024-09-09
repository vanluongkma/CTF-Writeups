use crate::verifier::Rp;
use num_bigint::{BigUint, RandomBits};
use rand::Rng;

pub fn rand_below(n: &BigUint) -> BigUint {
    let mut rng = rand::thread_rng();
    let bit = n.bits();

    loop {
        let y: BigUint = rng.sample(RandomBits::new(bit));
        if y < *n {
            return y;
        }
    }
}

pub fn bytes_to_biguint(bytes: &[u8]) -> BigUint {
    BigUint::from_bytes_be(bytes)
}

pub fn convert_rp_to_string(v: &[Rp]) -> Vec<String> {
    let mut normal_numbers = vec![];
    for item in v {
        match item {
            Rp::Tuple(a, b) => {
                normal_numbers.push(format!("({}, {})", a, b));
            }
            Rp::Number(n) => {
                normal_numbers.push(format!("{}", n));
            }
        }
    }
    normal_numbers
}
