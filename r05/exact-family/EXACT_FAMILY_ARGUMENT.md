# Why the predeclared adjacent-reversal rankings have C_R=1

Author argument, pending independent audit. The ranks are the increasing slot
order with any disjoint adjacent slot pairs reversed. Thus every relation
pointing left connects one reversed adjacent pair b=a+1 -> a. All relations
between different blocks point right, and each block has size one or two.

For any disjoint endpoint sets and allowed matching, a matching cost exceeds
the free sorted cost only if some positive slot gap is crossed both ways.
The leftward edge crossing that gap must be b -> a with b=a+1. Any disjoint
rightward edge p -> q crossing the same gap has p<a<b<q. Since those endpoints
belong to earlier/later blocks, both p -> a and b -> q are allowed. Swapping
the two targets therefore gives another allowed matching and reduces cost by
2(b-a)>0. A minimum allowed matching cannot have such an opposite crossing;
it attains the free lower bound. This holds for every admitted endpoint set,
so C_R=1. It covers all three declared first/last/all reversal families and
arbitrary increasing distinct slot geometry.

This short specialized argument also permits a cheaper recognition flag for
this designed family. It must be disclosed alongside any quartet gain: the
experiment exercises a possible general-recognizer use, not an optimality or
necessity claim. The measured Cheap route is the frozen R04 route and does
not contain a new family-specific flag.
