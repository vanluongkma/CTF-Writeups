use crate::utils::*;
use num_bigint::BigUint;
use serde_derive::Serialize;
pub struct Verifier {
    pub x: BigUint,
    pub y: BigUint,
    rs: Vec<Vec<(BigUint, BigUint)>>,
    pub pairs: Vec<Vec<(BigUint, BigUint)>>,
    pub num_rouns: usize,
}

#[derive(Serialize, Debug)]
pub enum Rp {
    Tuple(BigUint, BigUint),
    Number(BigUint),
}

impl Verifier {
    pub fn new(x: BigUint, y: BigUint, n: usize) -> Self {
        Verifier {
            x,
            y,
            rs: Vec::new(),
            pairs: Vec::new(),
            num_rouns: n,
        }
    }

    pub fn gen_w(&self, bit: i32, r: &BigUint) -> BigUint {
        if bit == 0 {
            r.modpow(&BigUint::from(2_u32), &self.x)
        } else {
            r.modpow(&BigUint::from(2_u32), &self.x) * &self.y % &self.x
        }
    }

    pub fn gen_pairs(&mut self) -> Vec<(BigUint, BigUint)> {
        let mut rr: Vec<(BigUint, BigUint)> = Vec::with_capacity(self.num_rouns);
        let mut pair: Vec<(BigUint, BigUint)> = Vec::with_capacity(self.num_rouns);
        for _ in 0..self.num_rouns {
            let r1 = rand_below(&self.x);
            let r2 = rand_below(&self.x);
            let a = r1.modpow(&BigUint::from(2_u32), &self.x);
            let b = r2.modpow(&BigUint::from(2_u32), &self.x) * &self.y % &self.x;

            pair.push((a, b));
            rr.push((r1, r2));
        }
        self.rs.push(rr.clone());
        self.pairs.push(pair.clone());
        pair
    }

    pub fn respond(&self, bit: &u32, list_i: Vec<u32>, r: &BigUint) -> Vec<Rp> {
        let mut v: Vec<Rp> = Vec::with_capacity(self.num_rouns);
        for (i, a) in list_i.iter().enumerate() {
            match (a, bit) {
                (&0, _) => {
                    let vj = &self.rs[self.rs.len() - 1][i];
                    v.push(Rp::Tuple(vj.0.clone(), vj.1.clone()));
                }
                (1, &0_u32) => {
                    let vj = r * &self.rs[self.rs.len() - 1][i].0 % &self.x;
                    v.push(Rp::Number(vj));
                }
                (1, &1_u32) => {
                    let vj = r * &self.rs[self.rs.len() - 1][i].1 * &self.y % &self.x;
                    v.push(Rp::Number(vj));
                }
                _ => panic!("Invalid input"),
            }
        }
        v
    }

    pub fn get_r(&self) -> BigUint {
        rand_below(&self.x)
    }
}
