use std::convert::TryInto;

/**
Apply a simple XOR cipher using they specified `key` of size 
`key_size`, to the `msg` char/byte array of size `msg_len`.

Writes he ciphertext to the externally allocated buffer `buf`.
*/
#[no_mangle]
/**pub fn cipher (msg: *const 18, key: *const 18, but: *mut 18, msg_len: usize, key_len: usize)
Executes the Rust-based cipher. The cipher-text should be written to buf by applying XOR to key and msg.**/
pub fn cipher(msg: *const i8, key: *const i8, buf: *mut i8,
  msg_len: usize, key_len: usize)
{
    let mut i: isize = 0;
    while i < msg_len.try_into().unwrap() {
      let key_len_isize: isize = key_len.try_into().unwrap();
      *buf.offset(i) = *msg.offset(i) ^ (*key.offset(i % key_len_isize));
      i = i + 1;
    }
}


