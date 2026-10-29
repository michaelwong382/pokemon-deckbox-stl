"""Round-3 remix of the Game Boy deck box: the signature engraved in the bottom reads "Yoojin" in script instead of "Ashwood".
Run from the repo root: python tools/round3_build.py   (needs trimesh, manifold3d, shapely, numpy, scipy, scikit-image, pillow)
Reads the second-round STLs from stl/remix/v2/ and the lettering from images/Elegant_Yoojin_Calligraphy.png;
writes the new body to stl/remix/v3/ and copies the unchanged lid and pin there.
Body coords (print orientation): X = depth (front face at +25.2), Y = width, Z = up, bottom face on the bed at Z = 0.
Seen from below with the front at the top, +Y points right: the lettering reads that way, as Ashwood's did.
"""
import os, shutil, trimesh, numpy as np, shapely.geometry as sg
from shapely.geometry.polygon import orient
from trimesh.creation import extrude_polygon
from PIL import Image
from scipy import ndimage as ndi
from skimage import morphology, measure
R="stl/remix/v2/"      # second-round files (input)
OUT="stl/remix/v3/"    # third-round files (output)
IMG="images/Elegant_Yoojin_Calligraphy.png"
os.makedirs(OUT,exist_ok=True)
body=trimesh.load(R+"Case-bottom_remix.stl",force='mesh')
ENG='manifold'
WIDTH=60.0        # lettering width (mm): the o's come out 5.7 mm tall, close to Ashwood's 6.0 mm
MIN_STROKE=0.6    # thinnest engraved line (mm); the image's hairlines would come out 0.3 mm, too fine to print in the bed face
FILLET=0.2        # radius (mm) rounding every inside corner of the outline: where widened hairlines meet thick strokes, and where strokes join
DEPTH=1.0        # engraving depth (mm), as Ashwood's: leaves 1 mm of floor above it
CX,CY=3.7,0.0     # centre of the flat bottom face (74 x 39 mm)
RES=0.01          # tracing resolution (mm per pixel)

# 1. fill Ashwood's 1 mm recess (it spans X -1.2..8.9, Y -20.4..20.5)
fill=trimesh.creation.box(bounds=[[-2.0,-21.5,0.0],[10.0,21.5,1.5]])
body3=body.union(fill,engine=ENG)

# 2. lettering: scale the image to RES, threshold, then widen only the strokes thinner than MIN_STROKE
#    (a MIN_STROKE-wide band along their centre line; thick strokes are left as drawn), smooth and trace the outlines
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
ink|=ndi.distance_transform_edt(~thin)*RES<=r
grown=ndi.distance_transform_edt(~ink)*RES<=FILLET  # closing with a FILLET-radius disk: rounds inside corners,
ink=ndi.distance_transform_edt(grown)*RES>FILLET    # leaves strokes and outside curves where they are
rows,cols=np.nonzero(ink); rc,cc=(rows.min()+rows.max())/2,(cols.min()+cols.max())/2
shape=sg.Polygon()
for c in measure.find_contours(ndi.gaussian_filter(ink.astype(float),0.05/RES),0.5):   # 0.05 mm blur smooths the pixel steps
    shape=shape.symmetric_difference(sg.Polygon(np.c_[CX-(c[:,0]-rc)*RES,CY+(c[:,1]-cc)*RES]))   # image down = -X, right = +Y
shape=shape.simplify(0.01)
parts=list(getattr(shape,'geoms',[shape]))
print("lettering bounds",np.round(shape.bounds,2).tolist(),"area",round(shape.area,1),"mm2,",len(parts),"parts,",
      sum(len(p.interiors) for p in parts),"counters")

# 3. engrave it DEPTH deep into the bottom face
cut=trimesh.util.concatenate([extrude_polygon(orient(p),DEPTH+1.0) for p in parts])
cut.apply_translation([0,0,-1.0])
body3=body3.difference(cut,engine=ENG)
body3.merge_vertices(); body3.update_faces(body3.nondegenerate_faces()); body3.remove_unreferenced_vertices()
print("Case-bottom_remix.stl","watertight",body3.is_watertight,"volume",round(body3.volume,1),"faces",len(body3.faces),"bounds",np.round(body3.bounds,2).tolist())
body3.export(OUT+"Case-bottom_remix.stl")
for name in ("Case-top_remix.stl","Hinge-pin_remix.stl"):   # unchanged from round 2
    shutil.copyfile(R+name,OUT+name)
