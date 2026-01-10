# Instant Insanity Puzzle

<https://en.wikipedia.org/wiki/Instant_Insanity>

Finding all winning permutations...

## Python

```shell
$ python3 --version
Python 3.12.3


$ time ./python/solve_v1.py

real    0m49,647s
user    0m49,541s
sys     0m0,034s


$ time ./python/solve_v2.py

real    0m32,177s
user    0m32,190s
sys     0m0,017s


$ time /opt/pypy3.11-v7.3.20-linux64/bin/pypy3 ./solve_v2.py

real    0m5,243s
user    0m5,149s
sys     0m0,080s
```

## Rust

```shell
cd rust/
cargo build -r
$ time ./target/release/cubes 

real    0m1,928s
user    0m1,911s
sys     0m0,005s
```
