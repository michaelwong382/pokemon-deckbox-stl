# Pikachu versions: the round-5 files with a drawing engraved 0.8 mm into the body's back wall, and optionally another on the lid's top face.
# Reads stl/remix/v5/ and images/pickachu/, writes a version folder (STLs + example_images/). Run with the venv python:
#   python -I tools/pickachu_build.py [design index] [output folder] [top=<design index>]
#   defaults: 5 (06_sitting_outline), stl/pickachu/v1_sitting_outline/, no top engraving.  Design indices are positions in P.DESIGNS (0 = 01).
import sys, os, shutil, trimesh, numpy as np, warnings; warnings.filterwarnings("ignore")
from scipy import ndimage
from skimage import measure
from shapely.geometry import Polygon, MultiPolygon
from trimesh.creation import extrude_polygon
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); import pickachu_samples as P
REPO=P.REPO; R=REPO+"stl/remix/v5/"; ENG='manifold'
args=[a for a in sys.argv[1:] if not a.startswith("top=")]; kw=dict(a.split("=",1) for a in sys.argv[1:] if "=" in a)
DESIGN=int(args[0]) if args else 5
OUT=(args[1] if len(args)>1 else REPO+"stl/pickachu/v1_sitting_outline/").rstrip("/")+"/"; IMGOUT=OUT+"example_images/"
TOP=int(kw["top"]) if "top" in kw else None
DEPTH=0.8                   # engraving depth (back wall 3.95 mm thick: X -17.75 outside, -13.8 inside; lid top 2.0 mm thick: Z 100.005 outside, 98.005 inside)
DILATE_MM=0.15              # thickens every stroke by this on each side (design 06: thinnest groove ~0.6 mm, median 0.8)
CLOSE_MM=0.45               # fills gaps between strokes narrower than this, which would print as slivers
MINSOLID=0.4                # mm: thinnest solid allowed between two grooves
MINSPECK=0.25               # mm2: smallest fragment kept when a design's lines drop out (a 0.56 mm dot)
BANDS=8                     # a fading engraving is cut as this many nested steps of DEPTH/BANDS
BACK=P.BACK_X; TOPZ=float(P.lid.bounds[1][2])   # the lid's top face, 100.005 in the box frame (the lid is 56.37 mm tall, not 56.36)
TOPPANEL=dict(y=(-33.0,33.0),z=(-21.0,13.5))   # the lid's top face: horizontal = Y, vertical = -X (image up points to the back). Flat face is X -16.1..23.5, Y +-37.3
CLOSEUP={5:(8,50.0),10:(-8,50.0),11:(-6,58.0),12:(-10,42.0),13:(-10,42.0),14:(-10,42.0)}.get(DESIGN,(0,45.0))    # (Y,Z) the close-up centres on: the face
def engraving_mask(design,panel=None):
    label,fname,crop,erase,pnl,rot,fade,drop,prune=P.spec(design); panel=panel or pnl; m=P.ink_mask(fname,crop,erase,rot)>0.5
    pl=P.placement(m,panel); mmpp=(pl[1]-pl[0])/m.shape[1]
    if drop or prune:
        if drop: m&=P.dropout_keep(m,pl,panel,drop)
        if prune: m&=P.prune_keep(m,pl,panel,prune)
        lab,n=ndimage.label(m); sizes=ndimage.sum(m,lab,range(1,n+1))*mmpp*mmpp      # a cut can leave specks too small to print
        m&=np.isin(lab,1+np.where(sizes>=MINSPECK)[0]); print("drop-out: %d fragments kept, %d specks under %.2f mm2 removed"%((sizes>=MINSPECK).sum(),(sizes<MINSPECK).sum(),MINSPECK))
    m=ndimage.binary_dilation(m,iterations=max(1,round(DILATE_MM/mmpp))); m=ndimage.binary_closing(m,iterations=max(1,round(CLOSE_MM/2/mmpp)))
    # any solid left between grooves thinner than MINSOLID becomes groove too (a nozzle can't lay it down anyway)
    r=int(round(MINSOLID/2/mmpp)); yy,xx=np.ogrid[-r:r+1,-r:r+1]; disk=(xx*xx+yy*yy)<=r*r
    bg=np.pad(~m,r+1,constant_values=True); bg=ndimage.binary_opening(bg,structure=disk)[r+1:-(r+1),r+1:-(r+1)]
    return label,~bg,panel,fade
def stroke_stats(b,mmpp):
    dt=ndimage.distance_transform_edt(b); sk=(dt>=ndimage.maximum_filter(dt,3)-1e-6)&b&(dt>0.5); return np.percentile(2*dt[sk]*mmpp,[2,50,98]).round(2)
def polygons(mask,pl,mirror=True):
    """Even-odd fill of the 0.5 iso-contours of the mask, in mm. Horizontal axis runs image-left to image-right as pl[1]->pl[0]
    when mirrored (the back wall, seen from behind) or pl[0]->pl[1] otherwise; vertical axis is pl[3] at the top row."""
    h,w=mask.shape; ay0,ay1,az0,az1=pl; pad=np.pad(mask.astype(float),2)
    polys=[]
    for c in measure.find_contours(pad,0.5):
        r,cc=c[:,0]-2,c[:,1]-2; U=(ay1-(cc+0.5)/w*(ay1-ay0)) if mirror else (ay0+(cc+0.5)/w*(ay1-ay0)); V=az1-(r+0.5)/h*(az1-az0)
        p=Polygon(np.stack([U,V],1)).simplify(0.015)
        if p.is_valid and p.area>0.05: polys.append(p)
    polys.sort(key=lambda p:-p.area); out=None
    for p in polys: out=p if out is None else out.symmetric_difference(p)
    out=out.buffer(0); return list(out.geoms) if isinstance(out,MultiPolygon) else [out]
BACK_T=np.array([[0,0,1,BACK-0.5],[1,0,0,0],[0,1,0,0],[0,0,0,1.0]])      # local (u,v,z) -> box (X=z-18.25, Y=u, Z=v): into the back wall
TOP_T=np.array([[0,-1,0,0],[1,0,0,0],[0,0,-1,TOPZ+0.5],[0,0,0,1.0]])    # local (u,v,z) -> box (X=-v, Y=u, Z=100.5-z): down into the lid's top
def cutter(polys,depth=None,T=BACK_T):
    depth=DEPTH if depth is None else depth; parts=[]
    for p in polys:
        e=extrude_polygon(p,height=depth+0.5)   # local z 0..depth+0.5: from 0.5 mm outside the surface to `depth` into it
        e.apply_transform(T); parts.append(e)
    return trimesh.util.concatenate(parts)
def report(old,new,expected):
    print("  watertight",new.is_watertight,"faces",len(new.faces),"volume removed %.1f mm3 (expected %.1f)"%(old.volume-new.volume,expected))
    removed=old.difference(new,engine=ENG); added=new.difference(old,engine=ENG)
    print("  removed bounds",removed.bounds.round(2).tolist(),"added volume %.4f"%(added.volume if len(added.faces) else 0))
def engrave_back(body):
    label,mask,panel,fade=engraving_mask(DESIGN); pl=P.placement(mask,panel); mmpp=(pl[1]-pl[0])/mask.shape[1]
    print("back wall:",label,"mask",mask.shape,"placed Y %.1f..%.1f Z %.1f..%.1f"%pl)
    print("  groove widths 2/50/98 pct (mm):",stroke_stats(mask,mmpp))
    if not fade:
        polys=polygons(mask,pl); area=sum(p.area for p in polys); print("  polygons",len(polys),"engraved area %.1f mm2"%area)
        new=body.difference(cutter(polys),engine=ENG); expected=area*DEPTH
    else:
        # depth = DEPTH * fade(Y,Z), cut as BANDS nested steps: step k reaches DEPTH*k/BANDS wherever fade >= k/BANDS
        f=P.fade_field(mask,pl,panel,fade); new=body; expected=0.0
        for k in range(1,BANDS+1):
            band=mask&(f>=k/BANDS-1e-6)
            if not band.any(): continue
            polys=polygons(band,pl); a=sum(p.area for p in polys); expected+=a*DEPTH/BANDS
            new=new.difference(cutter(polys,DEPTH*k/BANDS),engine=ENG); print("  step %d: depth %.2f mm over %.0f mm2, %d polygons"%(k,DEPTH*k/BANDS,a,len(polys)),flush=True)
        print("  fading engraving: expected volume %.1f mm3, full depth over the middle %.0f x %.0f mm"%(expected,pl[1]-pl[0]-2*fade,pl[3]-pl[2]-2*fade))
    report(body,new,expected); print("  wall left behind the engraving: %.2f mm"%((-13.8)-(BACK+DEPTH)))
    return new,pl,fade
def engrave_top(lid):
    label,mask,panel,fade=engraving_mask(TOP,TOPPANEL); pl=P.placement(mask,panel); mmpp=(pl[1]-pl[0])/mask.shape[1]
    print("lid top:",label,"mask",mask.shape,"placed Y %.1f..%.1f, X %.1f..%.1f"%(pl[0],pl[1],-pl[3],-pl[2]))
    print("  groove widths 2/50/98 pct (mm):",stroke_stats(mask,mmpp))
    polys=polygons(mask,pl,mirror=False); area=sum(p.area for p in polys); print("  polygons",len(polys),"engraved area %.1f mm2"%area)
    new=lid.difference(cutter(polys,T=TOP_T),engine=ENG); report(lid,new,area*DEPTH); print("  lid top left under the engraving: %.2f mm"%(TOPZ-DEPTH-(98.0+TOPZ-100.0)))
    return new,pl
def main():
    os.makedirs(IMGOUT,exist_ok=True)
    body=trimesh.load(R+"Case-bottom_remix.stl",force='mesh'); new,pl,fade=engrave_back(body); new.export(OUT+"Case-bottom_remix.stl")
    for f in os.listdir(R):
        if f.endswith(".stl") and f!="Case-bottom_remix.stl": shutil.copyfile(R+f,OUT+f)
    lid=P.lid; topfloor=None
    if TOP is not None:
        lid,tpl=engrave_top(P.lid); lp=lid.copy(); lp.apply_transform(np.linalg.inv(P.L2B)); lp.export(OUT+"Case-top_remix.stl")   # back to print orientation
        def topfloor(m):
            z=m.triangles_center[:,2]; isf=(m.face_normals[:,2]>0.99)&(z<TOPZ-0.005)&(z>TOPZ-DEPTH-0.01); return np.where(isf,0.62,1.0)
    # renders of the real geometry
    P.OUT=IMGOUT
    def floor(m):   # recess floors in the back wall, darkened in proportion to their depth
        x=m.triangles_center[:,0]; isf=(m.face_normals[:,0]<-0.99)&(x>BACK+0.005)&(x<BACK+DEPTH+0.01)
        return np.where(isf,1-0.38*np.clip((x-BACK)/DEPTH,0,1),1.0)
    pin=P.pin; B=(new,P.BODY,False,floor); LD=(lid,P.LID,False,topfloor); parts=[B,LD,(pin,P.PIN)]
    P.render(parts,"01_engraved_back.png",azim=180,elev=0,center=np.array([0,0,50.0]),radius=54)
    P.render(parts,"02_engraved_back_iso.png",azim=140,elev=22,light=(-0.6,0.3,0.75))
    cz=(pl[2]+pl[3])/2; P.render([B],"03_engraving_close_up.png",azim=160,elev=18,light=(-0.6,0.4,0.7),center=np.array([BACK,CLOSEUP[0],CLOSEUP[1]]),radius=16,ss=4)
    P.render([B],"04_engraving_raking_light.png",azim=180,elev=0,light=(-0.3,0.9,0.3),center=np.array([BACK,0,cz]),radius=(pl[3]-pl[2])/2+4,ss=4)
    if fade or P.spec(DESIGN)[7] or P.spec(DESIGN)[8]: P.render(parts,"05_fade_at_the_edge.png",azim=150,elev=10,light=(-0.5,0.6,0.6),center=np.array([BACK,-26,20.0]),radius=16,ss=4)
    if TOP is not None:
        P.render(parts,"06_top_from_the_front.png",azim=-35,elev=50,light=(0.3,-0.4,0.85))
        P.render([LD],"07_top_straight_down.png",azim=0,elev=90,up=[-1,0,0],light=(0.2,-0.3,0.95),center=np.array([3.7,0,TOPZ]),radius=42,ss=4)
    print("done")
if __name__=="__main__": main()
