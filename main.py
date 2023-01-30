from projectile import projectile

#environment constant
x = projectile(m = 15e-3, r = 0.01508, C = 0.75, rho = 1.293, g = 9.80665)
#get recorded data
x.getData("data.txt")
#get graph (x-axis, y-axis)
#choices: t, x, y, v, vx, vy, a, ax, ay
x.draw('x', 'y')