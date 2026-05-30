# Attribution

This project is a teaching demo of **ELIZA**, the program written by
**Joseph Weizenbaum** at MIT and described in his 1966 paper:

> Joseph Weizenbaum, *"ELIZA — A Computer Program For the Study of Natural
> Language Communication Between Man And Machine"*, Communications of the ACM,
> Vol. 9, No. 1 (January 1966), pp. 36–45.

The pattern-matching engine in `eliza/engine.py` is adapted from Wade Brainerd's
MIT-licensed Python port:

> https://github.com/wadetb/eliza — Copyright (c) 2019 Wade Brainerd, MIT License.

The original English `DOCTOR` script (`DOCTOR_EN` in `eliza/scripts.py`) is taken
from that repository. The German `DOCTOR` script (`DOCTOR_DE`) was written for
this project, following the same decomposition/reassembly conventions.
