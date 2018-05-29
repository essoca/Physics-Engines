The condition of equilibrium of an object is that the net external force acting on it must be zero. Since force is a vector, and we already know how to add vectors (to get the net or resultant), we can apply this knowledge to find the tensions of two strings that hold an object against gravity. ![Block hanging on a string](https://raw.githubusercontent.com/essoca/Physics-Engines/master/images/forces.png)

The condition of equilibrium require that the tensions (red vectors) in the left and right strings add up to the weight *mg*. By moving the points *p*<sub>*L*</sub> and *p*<sub>*R*</sub> and (without moving the block), which then require new strings to be attached, we can find the tensions as functions of the angles made with respect to the horizontal and as a function of weight.

We want to put enough weight---passed as an argument to the python script---and find the positions of for which the string(s) break. For this we need information about the [ultimate tensile strength](https://en.wikipedia.org/wiki/Ultimate_tensile_strength) of the strings. Taking nylon 6/6 for the strings, and assuming a cross-sectional area of 1*mm*<sup>2</sup>, the maximum tension supported before breaking is *T*<sub>*m*</sub> = 750 N.

Great! But how do we know where does a given string break? We can enforce that by adding a knot (a visible point randomly placed along the string). It is [known](https://www.researchgate.net/publication/264959195_The_rupture_of_knotted_strings_under_tension?tab=overview) that this reduces (down to 50%) the strength of the string and that the rupture takes place somewhere in the knot.

With this in mind, we want to break the string at the knot(s), and let the broken strings fall.

Have fun!
