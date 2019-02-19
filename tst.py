from ComputationalGeometry import *

pts1=PointSet((0,1),(1,3),(2,0))
pts2=PointSet((-2,3),(-1,-2),(0.5,1),(0.9,-1),(3,4),(2.5,0))
pts1.display()
yl=pts1.fitToLineSet(pts2)
# for fit in yl:
#     fit.display()
plt.show()

