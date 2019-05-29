# Getting Started

## Dependencies

- python (version 3.7.1+). It may be possible to run the code in previous versions, however not all functionality is guaranteed. See https://www.python.org for download instructions if python is not installed.

## Running the Program

There is no main funciton that runs our belief revision engine. The belief revision engine is primarily a module to import using either a python script or the python interpreter. The module should be imported as follows:

`from belief_revision_engine import cnf,belief_base,entails,expand,contract,revise`

An example file has been provided -  `example.py` - demonstrating the proper use of the module's functions. Only functions included in `belief_revision_engine.py` should be used; internal functions of any classes are not intended to be accessed by the user. There are comments at the beginning of each function detailing their behavior. The functions are restated for redundancy here.

### Functions
#### **`cnf(s)`**
- `s` - propositional logic sentence
- Converts a propositional sentence to Conjunctive Normal Form.

#### **`belief_base(s)`**
- `s` (optional) - propositional logic sentence in cnf
- Returns an instance of BeliefBase with `s` as the only held belief.

#### **`entails(b, s)`**
- `b` - belief base `s` - propositional logic sentence in cnf
- Return true or false if `b` entails `s`.

#### **`expand(b, s)`**
- `b` - belief base `s` - propositional logic sentence in cnf
- Expand `b` with `s`. Does not remove contradictions. Returns None.

#### **`contract(b, s, mode)`**
- `b` - belief base `s` - propositional logic sentence in cnf `mode` - type of contraction (*'partial-meet'* (default), *'full-meet'*, *'maxichoice'*)
- Contract `s` from `b`; remove all beliefs from `b` that entail `s`. Returns None.

#### **`revise(b, s, mode)`**
- `b` - belief base `s` - propositional logic sentence in cnf `mode` - type of contraction (*'partial-meet'* (default), *'full-meet'*, *'maxichoice'*)
- Revises `b` with `s`; remove all beliefs from `b` that entail not `s`, then expand `b` with `s`.

These functions can be used to formulate all aspects of a belief revision engine. Our unit tests are included in the source code and can be run from the command line. The working directory must be `src/` and the command to run is `python -m unittest -v`.

### Propositional Logic Symbols
We used the following symbols to represent propositional logic in our implementation of a belief revision engine:

| Symbol | Operation     |
|:------:|:--------------|
| `^`    | AND           |
| `v`    | OR            |
| `~`    | NOT           |
| `->`   | IMPLIES       |
| `<->`  | BICONDITIONAL |

***Note:*** It is imperative that parenthesis are used appropriately when using our cnf conversion tool. Statements like `p->q->r` are ambigious and are undefined in our engine. This should be replaced with `(p->q)->r` or `p->(q->r)`.


