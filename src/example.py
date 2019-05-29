from belief_revision_engine import belief_base,entails,expand,contract,revise

b = belief_base()
for beliefs in ['p','q^r']:
    expand(b, beliefs)
print("b is: {}".format(b))
revise(b, 'p^q')
print("after revision, b is: {}".format(b))
print("entails p? {}".format(entails(b,'p')))
expand(b, '~p^q')
contract(b,'p','full-meet')
print("after contraction, b is: {}".format(b))
print("entails p? {}".format(entails(b,'p')))
