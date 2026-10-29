"""Round-4 remix of the Game Boy deck box: buttons that push into the body by hand and stay put.
Run from the repo root: python tools/round4_build.py   (needs trimesh, manifold3d, shapely, numpy)
Reads the designer's D-Pad.stl, Button.stl and StartSelect.stl from stl/original/ and the round-3 files from stl/remix/v3/;
writes the new buttons to stl/remix/v4/ in print orientation and copies the unchanged body, lid and pin there.
Body coords: X = depth (front face at 25.2, inner face of the 4 mm front wall at 21.2), Y = width, Z = up. The designer's
button files are drawn in the box's own frame (Y up) in their assembled positions; O2R turns them into body coords.
The designer's buttons are the exact size of their seats. Here the parts that enter the seats are shrunk by CLEAR per side,
the D-pad and A/B pegs become crush-rib pegs (a loose core, four ribs that press in the 2.99 mm hole), and the Start/Select
pills, which have no peg, get one rib on each long side. Everything above the front face is left as drawn.
"""
import os, shutil, trimesh, numpy as np, shapely.geometry as sg
from shapely.geometry.polygon import orient
from trimesh.creation import extrude_polygon, revolve
ORIG="stl/original/"; R="stl/remix/v3/"; OUT="stl/remix/v4/"
os.makedirs(OUT,exist_ok=True)
ENG='manifold'
O2R=np.array([[1,0,0,3.7],[0,0,-1,0],[0,1,0,0],[0,0,0,1.0]])
FACE=25.2         # front face
CLEAR=0.15        # clearance per side between a button and its seat (mm)
CORNER=0.3        # radius on the D-pad cross's outer corners: printed seats have rounded inside corners
CORE_D,RIB_OD,RIB_W,RIB_N=2.6,3.1,0.5,4   # crush-rib peg for the 2.99 mm holes: loose core, ribs 0.055 mm proud per side
PEG_TIP,PEG_TOP=21.3,24.25                # peg from 0.1 mm short of the wall's inner face up into the base
PILL_RIB_W,PILL_RIB_PROUD=0.8,0.06        # Start/Select ribs: width, and how far they stand beyond the designer's outline
def load(nm): return trimesh.load(ORIG+nm+".stl",force='mesh').apply_transform(O2R)
def sec(m,x):
    s=m.section(plane_origin=[x,0,0],plane_normal=[1,0,0]); g=sg.Polygon()
    for e in s.entities:
        p=s.vertices[e.points][:,1:]
        if len(p)>=4: g=g.symmetric_difference(sg.Polygon(p).buffer(0))
    return max(getattr(g,'geoms',[g]),key=lambda q:q.area)
H2X=np.array([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1.0]])   # (Y,Z,height) -> (X,Y,Z)
def prism(poly,x0,x1):
    m=extrude_polygon(orient(poly),x1-x0); m.apply_transform(H2X); m.apply_translation([x0,0,0]); return m
def above_face(m):
    return m.intersection(trimesh.creation.box(bounds=[[FACE,-60,-10],[40,60,100]]),engine=ENG)
def peg(c):
    core=revolve([[0,0],[CORE_D/2-0.4,0],[CORE_D/2,0.4],[CORE_D/2,PEG_TOP-PEG_TIP],[0,PEG_TOP-PEG_TIP]],sections=48)
    core.apply_transform(H2X); core.apply_translation([PEG_TIP,0,0])
    parts=[core]
    for k in range(RIB_N):                     # ribs on the diagonals, clear of the hole's sagging top in the printed body
        a=np.radians(45+90*k); u=np.array([np.cos(a),np.sin(a)]); v=np.array([-u[1],u[0]])
        pts=[]
        for x,ro in ((PEG_TIP+0.6,CORE_D/2),(PEG_TIP+1.1,RIB_OD/2),(PEG_TOP,RIB_OD/2)):   # chamfered lead-in, then full height
            for ri in (CORE_D/2-0.3,ro):
                for t in (-RIB_W/2,RIB_W/2): pts.append([x,*(ri*u+t*v)])
        parts.append(trimesh.convex.convex_hull(np.array(pts)))
    m=parts[0]
    for p in parts[1:]: m=m.union(p,engine=ENG)
    m.apply_translation([0,c[0],c[1]]); return m
def finish(m,name,T):
    m.merge_vertices(); m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices()
    print(name,"watertight",m.is_watertight,"volume",round(m.volume,1),"faces",len(m.faces),"bounds",np.round(m.bounds,2).tolist())
    p=m.copy(); p.apply_transform(T); p.apply_translation(-p.bounds[0]*[1,1,1]+[-(p.bounds[1][0]-p.bounds[0][0])/2,-(p.bounds[1][1]-p.bounds[0][1])/2,0]); p.export(OUT+name)
FACE_DOWN=np.array([[0,1,0,0],[0,0,-1,0],[-1,0,0,0],[0,0,0,1.0]])   # top face on the bed, peg up (as the designer printed them)
BASE_DOWN=np.array([[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1.0]])    # back face on the bed, standing (as the designer printed them)

# D-pad: cross shrunk by CLEAR, outer corners rounded, from the seat floor at 24.2 to just above the face; new peg
d=load("D-Pad"); cross=sec(d,24.7); axis=sec(d,23.0).centroid.coords[0]
base=cross.buffer(-CLEAR,join_style=1).buffer(-CORNER).buffer(CORNER)
dpad=above_face(d).union(prism(base,24.2,FACE+0.05),engine=ENG).union(peg(axis),engine=ENG)
print("D-pad: cross %.2f -> %.2f mm2, peg axis"%(cross.area,base.area),np.round(axis,3))
finish(dpad,"D-Pad_remix.stl",FACE_DOWN)

# A/B button: cap shrunk to the seat's 7.994 mm minus clearance; new peg. Print two.
b=load("Button"); cap=sec(b,24.7); axis=sec(b,23.0).centroid.coords[0]
cap_d=2*np.sqrt(cap.area/np.pi); seat_d=7.994
base=sg.Point(cap.centroid).buffer(seat_d/2-CLEAR,resolution=48)
ab=above_face(b).union(prism(base,24.2,FACE+0.05),engine=ENG).union(peg(axis),engine=ENG)
print("A/B: cap %.3f mm in a %.3f seat -> base %.2f mm"%(cap_d,seat_d,2*(seat_d/2-CLEAR)))
finish(ab,"Button_remix.stl",FACE_DOWN)

# Start/Select: pill shrunk by CLEAR from the seat floor at 23.2, one rib on each long side. Print two.
s=load("StartSelect"); pill=sec(s,24.5); c=np.array(pill.centroid.coords[0])
rect=np.array(pill.minimum_rotated_rectangle.exterior.coords)[:4]; e=rect[1]-rect[0]; f=rect[2]-rect[1]
along=e if np.linalg.norm(e)>np.linalg.norm(f) else f; along=along/np.linalg.norm(along); across=np.array([-along[1],along[0]])
half=max(abs((np.array(pill.exterior.coords)-c)@across))          # half width of the pill
base=prism(pill.buffer(-CLEAR,join_style=1),23.2,FACE+0.05)
for side in (-1,1):
    pts=[]
    for x,out in ((23.5,half-CLEAR),(23.8,half+PILL_RIB_PROUD),(24.9,half+PILL_RIB_PROUD)):
        for a in (half-CLEAR-0.3,out):
            for t in (-PILL_RIB_W/2,PILL_RIB_W/2): pts.append([x,*(c+side*a*across+t*along)])
    base=base.union(trimesh.convex.convex_hull(np.array(pts)),engine=ENG)
ss=above_face(s).union(base,engine=ENG)
print("Start/Select: pill %.2f mm wide, slant %.0f deg, ribs %.2f mm proud of the base"%(2*half,np.degrees(np.arctan2(along[1],along[0]))%180,CLEAR+PILL_RIB_PROUD))
finish(ss,"StartSelect_remix.stl",BASE_DOWN)

for name in ("Case-bottom_remix.stl","Case-top_remix.stl","Hinge-pin_remix.stl"):   # unchanged from round 3
    shutil.copyfile(R+name,OUT+name)
