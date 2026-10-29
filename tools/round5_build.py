"""Round-5 remix of the Game Boy deck box: an engraving that prints reliably, a pin head recessed into the hinge (with a knock-out
hole at the other end), and fit-test coupons.
Run from the repo root: python tools/round5_build.py   (needs trimesh, manifold3d, shapely, numpy, scipy, scikit-image, pillow)
Reads the fourth-round files from stl/remix/v4/ and the lettering from images/Elegant_Yoojin_Calligraphy.png; writes stl/remix/v5/:
a new body and pin, the unchanged lid and buttons copied from round 4, and three test coupons cut from the new body and lid.
Body coords (print orientation): X = depth (front face at +25.2, inner face of the front wall at 21.2), Y = width, Z = up,
bottom face on the bed at Z = 0. Hinge axis at (X -22.2, Z 85.1) along Y; the body's end knuckles run to Y = ±30 and the
pin goes in at +Y (the left end, seen from the back). Pin coords (print orientation): X along its length, lying on a flat
side at Z = 0 with its axis at Z = 1.25; the head is at the -X end.
"""
import os, shutil, trimesh, numpy as np, shapely.geometry as sg
from shapely.geometry.polygon import orient
from trimesh.creation import extrude_polygon, revolve, cylinder, box
from trimesh.intersections import slice_mesh_plane
from PIL import Image
from scipy import ndimage as ndi
from skimage import morphology, measure
R="stl/remix/v4/"; OUT="stl/remix/v5/"; IMG="images/Elegant_Yoojin_Calligraphy.png"
os.makedirs(OUT,exist_ok=True); ENG='manifold'
body=trimesh.load(R+"Case-bottom_remix.stl",force='mesh'); lid=trimesh.load(R+"Case-top_remix.stl",force='mesh'); pin=trimesh.load(R+"Hinge-pin_remix.stl",force='mesh')
def finish(m,name,shift=(0,0,0)):
    m.merge_vertices(); m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices(); m.apply_translation(shift)
    print(name,"watertight",m.is_watertight,"volume",round(m.volume,1),"faces",len(m.faces),"bounds",np.round(m.bounds,2).tolist())
    m.export(OUT+name); return m

# ---- 1. Engraving: the round-3 lettering again, 0.8 mm deep instead of 1.0, and the loops under MIN_LOOP mm2 filled in.
#         Round 3's 0.6 mm hairlines left the two small loops at the tops of the o's as 1.3 mm islands of first-layer material,
#         1 mm tall, that a nozzle can knock off. The lettering is otherwise identical (same trace, centre and size).
WIDTH=60.0; MIN_STROKE=0.6; FILLET=0.2; DEPTH=0.8; MIN_LOOP=3.0; CX,CY=3.7,0.0; RES=0.01
fill=box(bounds=[[-9.0,-31.0,0.0],[16.5,31.0,1.2]])      # fills round 4's engraving (it spans X -8.4..15.8, Y ±30.2, Z 0..1)
body5=body.union(fill,engine=ENG)
g=np.asarray(Image.open(IMG).convert("L"))
ys,xs=np.nonzero(g<128); pad=8
im=Image.fromarray(g[ys.min()-pad:ys.max()+pad+1,xs.min()-pad:xs.max()+pad+1])
k=WIDTH/(xs.max()-xs.min()+1)/RES
ink=np.pad(np.asarray(im.resize((round(im.width*k),round(im.height*k)),Image.BICUBIC))<128,40)
lab,n=ndi.label(ink); a=ndi.sum(ink,lab,range(1,n+1))*RES**2
ink=np.isin(lab,1+np.flatnonzero(a>=0.05))           # drop specks
lab,n=ndi.label(~ink); a=ndi.sum(~ink,lab,range(1,n+1))*RES**2
ink|=np.isin(lab,1+np.flatnonzero(a<0.05))           # fill pinholes
r=MIN_STROKE/2
thin=morphology.skeletonize(ink)&(ndi.distance_transform_edt(ink)*RES<r)
ink|=ndi.distance_transform_edt(~thin)*RES<=r         # widen hairlines to MIN_STROKE
grown=ndi.distance_transform_edt(~ink)*RES<=FILLET    # round every inside corner to FILLET
ink=ndi.distance_transform_edt(grown)*RES>FILLET
lab,n=ndi.label(~ink); a=ndi.sum(~ink,lab,range(1,n+1))*RES**2
edge=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]).tolist())
small=[i for i in range(1,n+1) if a[i-1]<MIN_LOOP and i not in edge]
ink|=np.isin(lab,small)                                # fill the loops that would print as tiny islands
print("filled %d loops under %.1f mm2: %s mm2"%(len(small),MIN_LOOP,np.round(a[[i-1 for i in small]],2).tolist()))
rows,cols=np.nonzero(ink); rc,cc=(rows.min()+rows.max())/2,(cols.min()+cols.max())/2
shape=sg.Polygon()
for c in measure.find_contours(ndi.gaussian_filter(ink.astype(float),0.05/RES),0.5):
    shape=shape.symmetric_difference(sg.Polygon(np.c_[CX-(c[:,0]-rc)*RES,CY+(c[:,1]-cc)*RES]))   # image down = -X, right = +Y
shape=shape.simplify(0.01); parts=list(getattr(shape,'geoms',[shape]))
print("lettering bounds",np.round(shape.bounds,2).tolist(),"area",round(shape.area,1),"mm2,",len(parts),"parts,",sum(len(p.interiors) for p in parts),"loops")
cut=trimesh.util.concatenate([extrude_polygon(orient(p),DEPTH+1.0) for p in parts]); cut.apply_translation([0,0,-1.0])
body5=body5.difference(cut,engine=ENG)

# ---- 2. Pin head recessed into the +Y end knuckle. The knuckle is 3 mm in radius, so round 1's 5 x 3.75 mm head can't be
#         sunk into it; the round-5 pin gets a 4 mm round head with a flat bottom (so it still prints lying on its side), and
#         the knuckle a matching counterbore, 0.15 mm larger, with 0.85 mm of wall left round it. The far (-Y) knuckle's hole is
#         blind, closed from Y = -28.8, so the pin is also 1.5 mm shorter: its tail stays where round 1 put it, 0.3 mm short
#         of the blind end, while the head sits 1.7 mm deeper and finishes flush with the knuckle. With nothing to pull on,
#         the pin comes out the other way: a 1.6 mm hole through the blind end lets a paperclip push on the tail.
AXIS=np.array([-22.2,85.1]); Y_END=30.0; FLAT=83.85       # hinge axis (X,Z); end of the knuckle; the pin's flat side (shank bottom)
HEAD_R=2.0; HEAD_LEN=1.7; CLEAR=0.15; LEAD=0.2              # head radius and length; clearance round it; lead-in at the hole mouth
KNOCKOUT_D=1.6                                              # hole through the blind end so the pin can be pushed out (a paperclip fits)
FLOOR=Y_END-HEAD_LEN-0.02                                   # counterbore floor: the head finishes 0.02 mm inside the knuckle end
INWARD=[[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]]           # (x,y,z) -> (x,-z,y): a solid built along +z now runs along -Y
def inward(m,y_start): m.apply_transform(INWARD); m.apply_translation([AXIS[0],y_start,AXIS[1]]); return m
cb=cylinder(radius=HEAD_R+CLEAR,height=Y_END+1-FLOOR,sections=96); cb.apply_translation([0,0,(Y_END+1-FLOOR)/2])
cb=slice_mesh_plane(inward(cb,Y_END+1),plane_normal=[0,0,1],plane_origin=[0,0,FLAT-CLEAR],cap=True)   # from outside the end to the floor, flat-bottomed like the head
lead=inward(revolve([[0,-0.1],[1.4+LEAD+0.1,-0.1],[1.4+LEAD,0],[1.4,LEAD],[0,LEAD]],sections=96),FLOOR)   # 45-degree lead-in from the floor into the 2.8 mm hole
ko=cylinder(radius=KNOCKOUT_D/2,height=2.4,sections=48); ko.apply_translation([0,0,1.2]); ko=inward(ko,-28.6)   # through the blind end, Y -28.7..-31
body5=body5.difference(cb,engine=ENG).difference(lead,engine=ENG).difference(ko,engine=ENG)
body5=finish(body5,"Case-bottom_remix.stl")

# The pin: round 1's shank, drawn again as one convex hull (a regular octagon 2.5 mm across the flats, flat side down, with
# round 1's 0.41 mm chamfer at the tail), 1.5 mm shorter, with the new head unioned on. Pin X runs from the head (-X) to the
# tail (+X); once the pin is centred, box Y = 0.75 - pin X.
HEAD_X=-29.98; TAIL_X=28.48; CHAMFER=0.41; APOTHEM=1.25
def octagon(x,apothem):
    a=np.radians(22.5+45*np.arange(8)); r=apothem/np.cos(np.radians(22.5)); return np.c_[np.full(8,x),r*np.cos(a),1.25+r*np.sin(a)]
shank=trimesh.convex.convex_hull(np.vstack([octagon(HEAD_X+HEAD_LEN-0.1,APOTHEM),octagon(TAIL_X-CHAMFER,APOTHEM),octagon(TAIL_X,APOTHEM-CHAMFER)]))
head=cylinder(radius=HEAD_R,height=HEAD_LEN,sections=96); head.apply_transform([[0,0,1,0],[0,1,0,0],[-1,0,0,0],[0,0,0,1]])  # axis along X
head.apply_translation([HEAD_X+HEAD_LEN/2,0,1.25]); head=slice_mesh_plane(head,plane_normal=[0,0,1],plane_origin=[0,0,0],cap=True)   # flat bottom on the bed
pin5=shank.union(head,engine=ENG); pin5.apply_translation([-(pin5.bounds[0][0]+pin5.bounds[1][0])/2,0,0])
pin5=finish(pin5,"Hinge-pin_remix.stl")

# ---- 3. Fit-test coupons, cut from the new body and lid so the seats and hinge are exactly the real ones.
#         Each prints in the same orientation as the part it comes from, on a small foot where it needs one.
def coupon(m,b,foot=None,name=""):
    c=m.intersection(box(bounds=b),engine=ENG)
    if foot is not None: c=c.union(box(bounds=foot),engine=ENG)
    lo,hi=c.bounds; return finish(c,name,shift=[-(lo[0]+hi[0])/2,-(lo[1]+hi[1])/2,-lo[2]])
coupon(body5,[[21.0,-28,5.5],[27,29,39]],foot=[[19,-28,3.5],[27,29,5.55]],name="Test-seats.stl")          # front wall with all five seats
coupon(body5,[[-32,-33,74],[-12,33,90]],foot=[[-30,-33,72],[-10,33,74.05]],name="Test-hinge-body.stl")   # back wall top with the three body knuckles
coupon(lid,[[-40,-30,40.05],[40,30,51]],name="Test-hinge-lid.stl")                                        # lid's back wall with its two knuckles (lid print frame)

for name in ("Case-top_remix.stl","D-Pad_remix.stl","Button_remix.stl","StartSelect_remix.stl"):   # unchanged from round 4
    shutil.copyfile(R+name,OUT+name)
