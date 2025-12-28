# Instant Insanity Puzzle

<https://en.wikipedia.org/wiki/Instant_Insanity>

Finding all winning permutations...

## Python

```shell
$time ./python/solve_v1.py

Finished. Checked 8308800 combinations

real    0m26,314s
user    0m26,294s
sys     0m0,017s
```

```shell
$time ./python/solve_v2.py

Finished. Checked 8308800 combinations

real    0m18,542s
user    0m18,523s
sys     0m0,018s
```

```shell
$ /opt/pypy3.11-v7.3.19-linux64/bin/pypy3 python/solve_v2.py 

Finished. Checked 8308800 combinations

real    0m3,234s
user    0m3,181s
sys     0m0,052s
```

## Rust

```shell
cd rust/
cargo build -r
time ...
```
