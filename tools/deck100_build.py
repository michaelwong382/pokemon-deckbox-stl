"""100-card version of the Game Boy deck box remix: the round-5 box made 37 mm deeper inside (35 -> 72 mm) so it holds 100
double-sleeved cards (perfect-fit inner sleeve plus a standard outer sleeve). Width and height are unchanged: those sleeves are
the same 66-67 x 91-92 mm as single sleeves, and the round-5 inside of 70 x 96 mm already clears them.
Run from the repo root: python tools/deck100_build.py   (needs trimesh, manifold3d, shapely, numpy, scipy, scikit-image, pillow)
Reads the round-5 files from stl/remix/v5/ and the lettering from images/Elegant_Yoojin_Calligraphy.png; writes stl/100_deck_ver/:
a deeper body and lid, "Yoojin" engraved again in the middle of the longer bottom, and the pin, buttons and test coupons copied over
unchanged (the front wall and the hinge are the same, so the same coupons test them). The body starts from the round-4 body and
repeats round 5's three cuts (engraving, pin-head recess with its lead-in, knock-out hole) after deepening, with the hinge axis moved:
the recess and lead-in leave sliver faces in the end knuckle that the boolean engine mishandles if anything is cut afterwards on the
bigger mesh, so they have to come last. The result is round 5's body in every detail, just deeper.
Box coords: X = depth (front face at +25.2, inner face of the front wall at 21.2; the back wall and hinge move from X -17.75 to
-54.75, the hinge axis from X -22.2 to -59.2), Y = width, Z = up. The lid is worked on in box coords (L2B) and exported back in
its print orientation, front face down, so the lid's print frame is the same as before.

How the depth is added. The front wall with its buttons and notch, and the back wall with its hinge, are left exactly as they are:
every vertex behind the cut plane X = XC moves back by T, and the faces that span the cut (plain wall, floor and lid plate; neither
mesh has a vertex within 2 mm of the cut) just get longer. Two things run the whole depth at a slope and would get a kink from that:
the side seam where the lid's wall meets the body's wall, and the top of the body's inner wall (the "tongue" that runs up inside
the lid). Each is a plane in Z over X with the same back end. So each plane is rotated about its front edge to pass through the
moved back end, and every vertex belonging to one of the planes (the wall tops and the lid's matching bottom edges, the catch bead
and groove, the lid's lead-in chamfers) is moved vertically onto the rotated plane. Nothing else in the side walls has vertices at
those heights, so every wall face stays planar, and the catches keep their shape and their 17 mm from the front face.
"""
import os, shutil, trimesh, numpy as np, shapely.geometry as sg
from shapely.geometry.polygon import orient
from trimesh.creation import extrude_polygon, box, cylinder, revolve
from trimesh.intersections import slice_mesh_plane
from PIL import Image
from scipy import ndimage as ndi
from skimage import morphology, measure
R="stl/remix/v5/"; OUT="stl/100_deck_ver/"; IMG="images/Elegant_Yoojin_Calligraphy.png"
os.makedirs(OUT,exist_ok=True); ENG='manifold'
T=37.0            # extra depth (mm): 35 mm inside becomes 72
XC=-11.5          # cut plane: everything behind it (the hinge side) moves back by T
L2B=np.array([[0,0,-1,25.2],[-1,0,0,0],[0,1,0,71.82],[0,0,0,1.0]])   # lid print frame -> box frame
SEAM_F=(25.2,66.0); TONGUE_F=(23.2,73.93); BACK=(-15.65,85.0)   # (X,Z) front edges of the seam and tongue planes, and their common back end
WALL_Y=34.9       # the side walls are |Y| >= 35: inner wall 35..37 (the tongue), outer wall 37..39 (the seam)
FRONT_Y=29.5      # at the front corners both planes wrap onto the front face between the window frame and the corner: the tongue's lip (X 21.2..23.2) from |Y| 29.7, the seam's skin (X 23.2..25.2) from |Y| 31.5; the indicator-light dimple at Y -28.9 must stay put
def line(p,q): return lambda x: p[1]+(q[1]-p[1])*(x-p[0])/(q[0]-p[0])
zs,zt=line(SEAM_F,BACK),line(TONGUE_F,BACK)                                   # round-5 planes
zs2,zt2=line(SEAM_F,(BACK[0]-T,BACK[1])),line(TONGUE_F,(BACK[0]-T,BACK[1]))   # the same planes with the back end moved
print("seam slope %.4f -> %.4f, tongue slope %.4f -> %.4f"%((BACK[1]-SEAM_F[1])/(SEAM_F[0]-BACK[0]),(BACK[1]-SEAM_F[1])/(SEAM_F[0]-BACK[0]+T),
      (BACK[1]-TONGUE_F[1])/(TONGUE_F[0]-BACK[0]),(BACK[1]-TONGUE_F[1])/(TONGUE_F[0]-BACK[0]+T)))
def deepen(m,name):
    V=m.vertices.copy(); x,y,z=V[:,0],V[:,1],V[:,2]
    xn=np.where(x<XC,x-T,x)
    u=z-zs(x); ut=z-zt(x); g=zt(x)-zs(x)                      # height above the seam plane, above the tongue plane, and between them
    wall=(np.abs(y)>=WALL_Y)|((x>=21.2-1e-6)&(np.abs(y)>=np.where(x<=23.2+1e-6,FRONT_Y,FRONT_Y+1.0)))   # the side walls, plus the planes' wrap round the front corners
    band=wall&(x>BACK[0])&(x<=SEAM_F[0])&(z>60)
    seam=band&(z<85.15)&(u>=-0.1)&np.where(g>=3.4,u<=3.2,u<=0.3)   # on the seam plane (the lid's edge rides 0.23 above it), or the bead/groove 1.5-3.1 mm above it
    tongue=band&(z<BACK[1])&~seam&(ut>=-0.6)&(ut<=3.0)             # on the tongue plane, or the lid's inner-wall edge and chamfer just above it
    dz=np.where(seam,zs2(xn)-zs(x),np.where(tongue,zt2(xn)-zt(x),0.0))
    V[:,0]=xn; V[:,2]=z+dz
    print("%s: %d vertices moved back %g mm; %d re-sloped on the seam plane, %d on the tongue plane (largest move %.2f mm)"%(
          name,int((x<XC).sum()),T,int(seam.sum()),int(tongue.sum()),np.abs(dz).max()))
    return trimesh.Trimesh(V,m.faces.copy(),process=False)
def finish(m,name):
    m.merge_vertices(); m.update_faces(m.nondegenerate_faces()); m.remove_unreferenced_vertices()
    print(name,"watertight",m.is_watertight,"volume",round(m.volume,1),"faces",len(m.faces),"bounds",np.round(m.bounds,2).tolist())
    m.export(OUT+name); return m

# ---- 1. Body: deepen the round-4 body, fill its engraving and cut round 5's lettering again in the middle of the new bottom.
R4="stl/remix/v4/"
body=deepen(trimesh.load(R4+"Case-bottom_remix.stl",force='mesh'),"body")
fill=box(bounds=[[-9.0,-31.0,0.0],[16.5,31.0,1.2]])      # round 4's engraving spans X -8.4..15.8, Y +-30.2, Z 0..1
body=body.union(fill,engine=ENG)
WIDTH=60.0; MIN_STROKE=0.6; FILLET=0.2; DEPTH=0.8; MIN_LOOP=3.0; RES=0.01      # as round 5
CX,CY=(SEAM_F[0]+(-17.75-T))/2,0.0                                             # centre of the new bottom (front face 25.2, back face -54.75)
g=np.asarray(Image.open(IMG).convert("L"))
ys,xs=np.nonzero(g<128); pad=8
im=Image.fromarray(g[ys.min()-pad:ys.max()+pad+1,xs.min()-pad:xs.max()+pad+1])
k=WIDTH/(xs.max()-xs.min()+1)/RES
ink=np.pad(np.asarray(im.resize((round(im.width*k),round(im.height*k)),Image.BICUBIC))<128,40)
lab,n=ndi.label(ink); a=ndi.sum(ink,lab,range(1,n+1))*RES**2
ink=np.isin(lab,1+np.flatnonzero(a>=0.05))
lab,n=ndi.label(~ink); a=ndi.sum(~ink,lab,range(1,n+1))*RES**2
ink|=np.isin(lab,1+np.flatnonzero(a<0.05))
r=MIN_STROKE/2
thin=morphology.skeletonize(ink)&(ndi.distance_transform_edt(ink)*RES<r)
ink|=ndi.distance_transform_edt(~thin)*RES<=r
grown=ndi.distance_transform_edt(~ink)*RES<=FILLET
ink=ndi.distance_transform_edt(grown)*RES>FILLET
lab,n=ndi.label(~ink); a=ndi.sum(~ink,lab,range(1,n+1))*RES**2
edge=set(np.unique(np.r_[lab[0],lab[-1],lab[:,0],lab[:,-1]]).tolist())
small=[i for i in range(1,n+1) if a[i-1]<MIN_LOOP and i not in edge]
ink|=np.isin(lab,small)
rows,cols=np.nonzero(ink); rc,cc=(rows.min()+rows.max())/2,(cols.min()+cols.max())/2
shape=sg.Polygon()
for c in measure.find_contours(ndi.gaussian_filter(ink.astype(float),0.05/RES),0.5):
    shape=shape.symmetric_difference(sg.Polygon(np.c_[CX-(c[:,0]-rc)*RES,CY+(c[:,1]-cc)*RES]))   # image down = -X, right = +Y
shape=shape.simplify(0.01); parts=list(getattr(shape,'geoms',[shape]))
print("lettering centred at X %.2f: bounds"%CX,np.round(shape.bounds,2).tolist(),"area",round(shape.area,1),"mm2")
cut=trimesh.util.concatenate([extrude_polygon(orient(p),DEPTH+1.0) for p in parts]); cut.apply_translation([0,0,-1.0])
body=body.difference(cut,engine=ENG)
# round 5's hinge cuts, last: the recess for the pin head in the +Y end knuckle with its lead-in, and the knock-out hole at -Y
AXIS=np.array([-22.2-T,85.1]); Y_END=30.0; FLAT=83.85; HEAD_R=2.0; HEAD_LEN=1.7; CLEAR=0.15; LEAD=0.2; KNOCKOUT_D=1.6
FLOOR=Y_END-HEAD_LEN-0.02
INWARD=[[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]]
def inward(m,y_start): m.apply_transform(INWARD); m.apply_translation([AXIS[0],y_start,AXIS[1]]); return m
cb=cylinder(radius=HEAD_R+CLEAR,height=Y_END+1-FLOOR,sections=96); cb.apply_translation([0,0,(Y_END+1-FLOOR)/2])
cb=slice_mesh_plane(inward(cb,Y_END+1),plane_normal=[0,0,1],plane_origin=[0,0,FLAT-CLEAR],cap=True)
lead=inward(revolve([[0,-0.1],[1.4+LEAD+0.1,-0.1],[1.4+LEAD,0],[1.4,LEAD],[0,LEAD]],sections=96),FLOOR)
ko=cylinder(radius=KNOCKOUT_D/2,height=2.4,sections=48); ko.apply_translation([0,0,1.2]); ko=inward(ko,-28.6)
body=body.difference(cb,engine=ENG).difference(lead,engine=ENG).difference(ko,engine=ENG)
body=finish(body,"Case-bottom_remix.stl")

# ---- 2. Lid: the same move in box coords, then back to its print orientation (front face on the bed, as before).
lid=trimesh.load(R+"Case-top_remix.stl",force='mesh'); lid.apply_transform(L2B)
lid=deepen(lid,"lid"); lid.apply_transform(np.linalg.inv(L2B))
lid=finish(lid,"Case-top_remix.stl")

# ---- 3. Unchanged parts: the pin, the buttons and the three fit-test coupons (the front wall and hinge they test are the same).
for name in ("Hinge-pin_remix.stl","D-Pad_remix.stl","Button_remix.stl","StartSelect_remix.stl","Test-seats.stl","Test-hinge-body.stl","Test-hinge-lid.stl"):
    shutil.copyfile(R+name,OUT+name)
print("copied the pin, three button files and three coupons from round 5")
