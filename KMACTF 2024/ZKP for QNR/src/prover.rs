use num_bigint::BigUint;
use rand::Rng;

pub struct Prover {
    pub x: BigUint,
    pub y: BigUint,
    pub num_rounds: usize,
    pub list_i: Vec<Vec<u32>>,
}

impl Prover {
    pub fn new(x: BigUint, y: BigUint, n: usize) -> Self {
        Prover {
            x,
            y,
            num_rounds: n,
            list_i: Vec::new(),
        }
    }

    pub fn gen_list_i(&self) -> Vec<u32> {
        let mut rng = rand::thread_rng();
        let list_i: Vec<u32> = (0..self.num_rounds).map(|_| rng.gen_range(0..2)).collect();
        list_i
    }

    // I forgot to implement verify function
    // pub fn verify() -> {
    //
    // }
}
