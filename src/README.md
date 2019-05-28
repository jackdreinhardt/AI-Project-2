# Getting Started

## Dependencies

- python (version 3.7.1+). It may be possible to run the code in previous versions, however not all functionality is guaranteed. See https://www.python.org for download instructions if python is not installed.

## Running the Program

There is no main file to run for the belief revision engine. The belief revision engine is primarily a module to import using either a python script or the python interpreter. An example file has been provided -  `example.py` - demonstrating the proper use of the module's functions. Only functions included in `belief_revision_engine.py` should be used; internal functions of any classes are not intended to be accessed by the user. There are comments at the beginning of each function detailing their behavior. The functions are restated for redundancy here.

### Functions
#### **`cnf(s)`**
- `s` - propositional logic sentence
- Converts a propositional sentence to Conjunctive Normal Form.

#### **`belief_base(s)`**
- `s` (optional) - propositional logic sentence
- Returns an instance of BeliefBase with `s` as the only held belief.

#### **`entails(b, s)`**
- `b` - belief base `s` - propositional logic sentence
- Return true or false if `b` entails `s`.

#### **`expand(b, s)`**
- `b` - belief base `s` - propositional logic sentence
- Expand `b` with `s`. Does not remove contradictions. Returns None.

#### **`contract(b, s, mode)`**
- `b` - belief base `s` - propositional logic sentence `mode` - type of contraction (*'partial-meet'*, *'full-meet'*, *'maxichoice'*)
- Contract `s` from `b`; remove all beliefs from `b` that entail `s`. Returns None.

#### **`revise(b, s, mode)`**
- `b` - belief base `s` - propositional logic sentence `mode` - type of contraction (*'partial-meet'*, *'full-meet'*, *'maxichoice'*)
- Revises `b` with `s`; remove all beliefs from `b` that entail not `s`, then expand `b` with `s`.



