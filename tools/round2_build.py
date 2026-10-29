"""Round-2 remix of the Game Boy deck box: thick screen frame, snap catches, thumb notch, lead-in chamfers.
Run from the repo root: python tools/round2_build.py   (needs trimesh, manifold3d, shapely, numpy)
Reads the first-round STLs from stl/remix/v1/ and writes the new lid and body to stl/remix/v2/.
Lid coords (print orientation): X = box width (box Y = -X), Y = box height (box Z = Y + 71.82), Z = depth from front face (box X = 25.2 - Z).
Body coords (print orientation): X = depth (front face at +25.2), Y = width, Z = up.
"""
import trimesh, numpy as np, shapely.geometry as sg, shapely.affinity as sa, shapely.ops as so
from trimesh.creation import extrude_polygon
R="stl/remix/v1/"      # first-round files (input)
OUT="stl/remix/v2/"    # second-round files (output)
import os; os.makedirs(OUT,exist_ok=True)
lid=trimesh.load(R+"Case-top_remix.stl",force='mesh')
body=trimesh.load(R+"Case-bottom_remix.stl",force='mesh')
ENG='manifold'
def union(a,b): return a.union(b,engine=ENG)
def diff(a,b): return a.difference(b,engine=ENG)
def hull(pts): return trimesh.convex.convex_hull(np.array(pts,dtype=float))
def loops2d(m,axis,val,keep):
    n=np.zeros(3);n[axis]=1;o=np.zeros(3);o[axis]=val
    s=m.section(plane_origin=o,plane_normal=n)
    out=[]
    for ent in s.entities:
        pts=s.vertices[ent.points][:,keep]
        p=sg.Polygon(pts)
        if not p.is_valid: p=p.buffer(0)
        out.append(p)
    return out

# ---------------- LID ----------------
# outline of the front plate at Z=1 (lid X,Y): biggest polygon = outer outline, window = the other
polys=loops2d(lid,2,1.0,[0,1])
polys.sort(key=lambda p:-p.area)
outline,window=polys[0],polys[1]
print("outline bounds",outline.bounds,"window bounds",window.bounds)
# thick slab: outline clipped to |X|<=29.5 and Y<=26.18 (ceiling), minus the window
SLAB_HALFW=29.5; CEIL=26.18; SLAB_Z0=1.7; SLAB_Z1=4.0
slab_poly=outline.intersection(sg.box(-SLAB_HALFW,-40,SLAB_HALFW,CEIL)).difference(window)
slab=extrude_polygon(slab_poly,SLAB_Z1-SLAB_Z0); slab.apply_translation([0,0,SLAB_Z0])
lid2=union(lid,slab)
# bottom bar inner-bottom edge chamfer (1 mm, 45 deg): pushes a bowed front card back instead of pinching it at the seam
bar=hull([p for sx in (-1,1) for p in ((sx*29.6,-28.5,4.5),(sx*29.6,-26.68,4.5),(sx*29.6,-28.5,2.68))])
lid2=diff(lid2,bar)
# ceiling lead-in chamfer: from (Y=21.68,Z=4.0) to (Y=26.18,Z=1.2), across |X|<35
Yc0,Yc1,Zc1=21.68,26.18,1.2
wedge=hull([p for sx in (-1,1) for p in ((sx*35.0,Yc0,SLAB_Z1),(sx*35.0,Yc0,6.0),(sx*35.0,Yc1,Zc1),(sx*35.0,Yc1,6.0))])
lid2=diff(lid2,wedge)
# side-wall inner-layer lead-in chamfer (1.2 mm) along the sloped bottom edge, Z from 1.89 to 40
P1=np.array([2.27,1.80]); P2=np.array([13.38,40.09]); d=(P2-P1)/np.linalg.norm(P2-P1)
def on_line_at_Z(z): return P1+d*((z-P1[1])/d[1])
A=on_line_at_Z(1.89); B=on_line_at_Z(40.0); CH=1.2
for sx in (-1,1):
    pr=hull([(sx*35.0,A[0],A[1]),(sx*35.0,B[0],B[1]),(sx*35.0,A[0]+CH,A[1]),(sx*35.0,B[0]+CH,B[1]),
             (sx*(35.0+CH),A[0],A[1]),(sx*(35.0+CH),B[0],B[1])])
    lid2=diff(lid2,pr)
# back-wall inner-bottom chamfer (1.5 mm): edge at (Y=13.38, Z=40.0)
CB=1.5
pr=hull([(sx*36.95,13.38,40.0) for sx in (-1,1)]+[(sx*36.95,13.38+CB,40.0) for sx in (-1,1)]+[(sx*36.95,13.38,40.0+CB) for sx in (-1,1)])
lid2=diff(lid2,pr)
# latch grooves in the outer layer's inner face (|X|=36.95): 8 x 1.4, 0.4 deep (to |X|=37.35), centred at box (X=8,Z=76.3)
LATCH_BX,LATCH_BZ=8.0,76.3
gz=25.2-LATCH_BX; gy=LATCH_BZ-71.82
seam=np.array([0.0,-18.37,-39.49]); seam/=np.linalg.norm(seam)   # lid (X,Y,Z) direction of the seam
ang=np.arctan2(seam[1],seam[2])  # rotate +Z toward this direction about X: rot_x(phi) maps (0,0,1)->(0,-sin phi,cos phi)
for sx in (-1,1):
    g=trimesh.creation.box(extents=[0.45,1.4,9.0])
    g.apply_transform(trimesh.transformations.rotation_matrix(-ang,[1,0,0]))
    g.apply_translation([sx*(36.9+0.225),gy,gz])   # spans |X| 36.9..37.35
    lid2=diff(lid2,g)
# ---------------- BODY ----------------
# 1. cut the tongue layer (X 21.2-23.2) flush with the middle layer's top (Z=43.43) wherever the lid's thick slab sits (+0.2 clearance)
tc=trimesh.creation.box(extents=[2.7,2*(SLAB_HALFW+0.2),40.0])
tc.apply_translation([20.5+1.35,0,43.43+20.0])
body2=diff(body,tc)
# 2. thumb notch: semi-ellipse 22 wide x 7 tall under the seam, floor sloping to 2.6 mm deep at the seam
SEAM_Z=43.43; NW,NH,ND=11.0,7.0,2.6
pts=[]
for t in np.linspace(np.pi,2*np.pi,61):
    y=NW*np.cos(t); z=SEAM_Z+NH*np.sin(t)
    xf=25.2-ND*(z-(SEAM_Z-NH))/NH
    pts+= [(xf,y,z),(27.0,y,z)]
pts+= [(25.2-ND,-NW,SEAM_Z+2),(25.2-ND,NW,SEAM_Z+2),(27.0,-NW,SEAM_Z+2),(27.0,NW,SEAM_Z+2)]
body2=diff(body2,hull(pts))
# 3. snap beads on the inner layer's outer face (Y=+-37.0): elliptical cylinder r=0.6 (in-plane) x 0.3 (out), 8 long along the seam
seam_b=np.array([39.49,0,-18.37]); seam_b/=np.linalg.norm(seam_b)
for sy in (-1,1):
    c=trimesh.creation.cylinder(radius=0.6,height=8.0,sections=48)   # axis along Z
    c.apply_transform(trimesh.transformations.rotation_matrix(0,[1,0,0]))
    # align Z axis to seam_b
    T=trimesh.geometry.align_vectors([0,0,1],seam_b)
    c.apply_transform(T)
    # squash in Y to 0.3
    c.apply_transform(np.diag([1,0.5,1,1.0]))
    c.apply_translation([LATCH_BX,sy*37.0,LATCH_BZ])
    body2=union(body2,c)
for name,m in (("Case-top_remix.stl",lid2),("Case-bottom_remix.stl",body2)):
    m.merge_vertices(); m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices()
    print(name,"watertight",m.is_watertight,"volume",round(m.volume,1),"faces",len(m.faces),"bounds",np.round(m.bounds,2).tolist())
    m.export(OUT+name)
