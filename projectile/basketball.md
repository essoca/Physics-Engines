Projectile motion
=================

Projectile motion is a combination of a horizontal motion at constant speed (if we neglect air resistance) and a vertical motion at constant acceleration due to gravity.

*x* = *x*<sub>0</sub> + *v*<sub>0*x*</sub>*t*
$$y=y\_0+v\_{0y}t-\\tfrac{1}{2}gt^2$$
 ![Projectile motion](https://raw.githubusercontent.com/essoca/Physics-Engines/master/images/projectile.png)

**The curved described is a parabola**

If we let (*x*, *y*) represent the coordinates of an object which is launched at a velocity $\\vec{v}\_0$, making an angle *θ* with the horizontal, the equation of the parabola can be shown to be

$$y=(\\tan\\theta)x-\\Bigl(\\dfrac{g}{2v\_0^2\\cos^2\\theta}\\Bigr)x^2$$

### Let's play basketball

We want to place the center of the basket at the coordinates (*x*<sub>*b*</sub>, *y*<sub>*b*</sub>) and let the ball pass through this center at an angle of −45<sup>∘</sup>. The speed and angle required for this is

$$v\_0=\\sqrt{\\dfrac{g\[x\_b^2+(2y\_b+x\_b)^2\]}{2(x\_b+y\_b)}}$$
*θ* = tan<sup>−1</sup>(1 + 2*y*<sub>*b*</sub>/*x*<sub>*b*</sub>)
 Great! So now throw a ball at this speed and angle in Pygame, track its trajectory, and show that it passes through the center of the basket.

![Basketball scoring](https://raw.githubusercontent.com/essoca/Physics-Engines/master/images/bouncing.png)

The center of the basket should appear at random on the screen, and the ball cannot exceed the boundaries defined by the screen size. Also, note that the above equations are derived after defining positive *y* upwards and positive *x* to the right.
