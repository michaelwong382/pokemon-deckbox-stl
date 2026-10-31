# Preview renders of the Pikachu line art from images/pickachu/ laid on the back wall of the round-5 box.
# Writes stl/pickachu/: a back elevation and a back iso view per design, plus a contact sheet.
# The art is drawn as dark lines on the body's back face (box frame X = -17.75, Y +-35.6, Z 1.6..85); nothing is cut into the mesh.
import sys, os, trimesh, numpy as np, warnings; warnings.filterwarnings("ignore")
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageDraw, ImageFont
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+"/"; R=REPO+"stl/remix/v5/"; IMG=REPO+"images/pickachu/"
OUT=sys.argv[1] if len(sys.argv)>1 else REPO+"stl/pickachu/"
L2B=np.array([[0,0,-1,25.2],[-1,0,0,0],[0,1,0,71.82],[0,0,0,1.0]]); P2B=np.array([[0,1,0,-22.2],[-1,0,0,0.75],[0,0,1,83.85],[0,0,0,1.0]])
body=trimesh.load(R+"Case-bottom_remix.stl",force='mesh'); lid=trimesh.load(R+"Case-top_remix.stl",force='mesh'); pin=trimesh.load(R+"Hinge-pin_remix.stl",force='mesh')
lid.apply_transform(L2B); pin.apply_transform(P2B)
BACK_X=-17.75                                   # plane of the body's back wall
PANEL=dict(y=(-30.0,30.0),z=(6.0,78.0))         # where a single figure goes: 60 x 72 mm, ~5.6 mm in from the edges
WALL=dict(y=(-33.0,33.0),z=(3.0,75.0))          # nearly the whole plain wall, for all-over patterns: 66 x 72 mm. The 45-degree support wedge under the hinge knuckles meets the wall at Z = 76.4, so nothing may go higher
WALLFULL=dict(y=(-35.6,35.6),z=(1.6,76.0))      # the whole flat wall, edge to edge, for a pattern that fades out towards the edges
# (label, source file, crop box in source pixels or None, boxes to blank out inside the crop, panel override, rotation in degrees)
DESIGNS=[
 ("01_waving",            "il_1588xN.7897305927_3qdi.webp", None),
 ("02_jumping",           "il_1588xN.7435648637_o518.webp", None),
 ("03_standing_smile",    "il_1588xN.8249798320_c1d0.webp", None),
 ("04_standing_laughing", "il_1588xN.8268143871_6cok.webp", None),
 ("05_sitting_bold",      "s-l1600.jpg", None),
 ("06_sitting_outline",   "Pikachu-I-01-scaled.jpg", (133,160,1263,1277)),
 ("07_head",              "Pikachu-I-01-scaled.jpg", (1303,1170,2461,2180)),
 ("08_face",              "Pikachu-I-01-scaled.jpg", (253,1583,1130,2180)),
 ("09_cap",               "1-1.webp", None),
 ("10_pokeball",          "Pikachu-I-01-scaled.jpg", (1463,400,2434,1330), [(0,800,110,930)]),   # blank the ear tip of the head next to it
 # an all-over pattern: a portrait window centred on Pikachu, run nearly edge to edge (66 x 72 mm)
 ("11_berries",           "11_pickachu_berries_outline.png", (290,0,1229,1024), [], WALL),
 # the same drawing turned 90 degrees anticlockwise so its long side runs up the box (Pikachu's head at the top), cropped to the wall's shape
 ("12_berries_rotated",   "11_pickachu_berries_outline.png", (0,201,1024,1318), [], WALL, 90),
 # upright again, but over the whole wall, with the engraving fading to nothing over the last 10 mm before each edge
 ("13_berries_fade",      "11_pickachu_berries_outline.png", (270,0,1250,1024), [], WALLFULL, 0, 10.0),
 # the same, full depth everywhere, but the lines break up and drop out over the last 12 mm before each edge
 ("14_berries_dropout",   "11_pickachu_berries_outline.png", (270,0,1250,1024), [], WALLFULL, 0, 0.0, 12.0),
 # the same, full depth, but thinned out towards the edges by removing whole line segments (junction to junction) while keeping the drawing connected
 ("15_berries_pruned",    "11_pickachu_berries_outline.png", (270,0,1250,1024), [], WALLFULL, 0, 0.0, 0.0, 14.0),
]
def spec(i):
    """(label, file, crop, erase boxes, panel, rotation, fade width, drop-out width, prune width) for design i, with defaults filled in."""
    d=list(DESIGNS[i])+[None]*(9-len(DESIGNS[i])); return d[0],d[1],d[2],d[3] or [],d[4] or PANEL,d[5] or 0,d[6] or 0.0,d[7] or 0.0,d[8] or 0.0
def prune_keep(mask,pl,panel,width,seed=15):
    """Boolean: which pixels of the drawing survive when the line network is thinned towards the edges.
    The drawing is skeletonised and split into segments between junctions. Going from the edge inwards, each segment is
    removed with probability 1 - d/width (d = its distance from the nearest edge), but only whole and only if the lines it
    joined stay connected without it; a segment that would split the drawing is kept. Nothing is ever cut mid-line."""
    if not width: return None
    from scipy import ndimage
    from skimage.morphology import skeletonize
    ink=mask>0.5; h,w=ink.shape; mmpp=(pl[1]-pl[0])/w; rng=np.random.default_rng(seed)
    sk=skeletonize(ink); nb=ndimage.convolve(sk.astype(int),np.ones((3,3),int),mode='constant')-1
    junc=sk&(nb>=3); juncd=ndimage.binary_dilation(junc,structure=np.ones((3,3),bool))
    jl,nj=ndimage.label(juncd&sk,structure=np.ones((3,3)))                    # junction clusters
    sl,ns=ndimage.label(sk&~juncd,structure=np.ones((3,3)))                   # segments between them
    comp,_=ndimage.label(ink,structure=np.ones((3,3)))                        # original connected pieces of the drawing
    dist=edge_distance(mask,pl,panel)
    # which junctions does each segment touch?  (dilate each segment by one pixel and look for junction labels)
    ends=[set() for _ in range(ns+1)]
    sd=ndimage.grey_dilation(sl,size=(3,3)); hit=(jl>0)&(sd>0)
    for sgl,jj in zip(sd[hit],jl[hit]): ends[sgl].add(int(jj))
    # a segment's distance from the edge: the mean over its pixels
    segd=ndimage.mean(dist,sl,range(1,ns+1)); segc=ndimage.maximum(comp,sl,range(1,ns+1))
    alive=np.ones(ns+1,bool); alive[0]=False
    adj={}
    def rebuild():
        adj.clear()
        for sgl in range(1,ns+1):
            if not alive[sgl]: continue
            e=list(ends[sgl])
            for a in e:
                for b in e:
                    if a!=b: adj.setdefault(a,set()).add(b)
    def connected(a,b):     # are junctions a and b joined by surviving segments?
        seen={a}; stack=[a]
        while stack:
            x=stack.pop()
            if x==b: return True
            for y in adj.get(x,()):
                if y not in seen: seen.add(y); stack.append(y)
        return False
    order=np.argsort(segd)+1; removed=0; kept_bridge=0; rebuild()
    for sgl in order:
        d=segd[sgl-1]; p=min(d/width,1.0)
        if rng.random()<p: continue                                           # survives by chance (always, beyond `width`)
        e=list(ends[sgl])
        if len(e)==2:
            # take it out, test, put back if the two junctions lose each other
            alive[sgl]=False; rebuild()
            if not connected(e[0],e[1]): alive[sgl]=True; rebuild(); kept_bridge+=1; continue
        else:
            alive[sgl]=False                                                  # a dangling or isolated piece: whole thing goes
        removed+=1
    rebuild()
    keep_sk=sk&((sl==0)|alive[sl])                                            # surviving skeleton (junctions always stay)
    # a surviving line keeps its full width: every ink pixel within the local half-width of a surviving skeleton pixel stays
    hw=ndimage.distance_transform_edt(ink)
    dd,(iy,ix)=ndimage.distance_transform_edt(~keep_sk,return_indices=True)
    keep=ink&(dd<=hw[iy,ix]+0.5)
    print("prune: %d segments, %d removed, %d kept to stay connected, %d junctions"%(ns,removed,kept_bridge,nj),flush=True)
    return keep
def edge_distance(mask,pl,panel):
    """Per-pixel distance (mm) from the nearest edge of the panel."""
    h,w=mask.shape; ay0,ay1,az0,az1=pl; Y=ay1-(np.arange(w)+0.5)/w*(ay1-ay0); Z=az1-(np.arange(h)+0.5)/h*(az1-az0)
    (py0,py1),(pz0,pz1)=panel['y'],panel['z']; dy=np.minimum(Y-py0,py1-Y); dz=np.minimum(Z-pz0,pz1-Z); return np.minimum(dy[None,:],dz[:,None])
def dropout_keep(mask,pl,panel,width,seed=14,cell_mm=3.0):
    """Boolean: which pixels of the drawing survive. A smooth random field (features ~cell_mm) is thresholded against the
    distance to the edge, so strokes drop out in fragments, more of them the nearer the edge; all survive beyond `width` mm."""
    if not width: return None
    from scipy import ndimage
    h,w=mask.shape; mmpp=(pl[1]-pl[0])/w; rng=np.random.default_rng(seed)
    cells=(int(np.ceil(h*mmpp/cell_mm))+3,int(np.ceil(w*mmpp/cell_mm))+3)
    n=ndimage.zoom(rng.standard_normal(cells),(h/cells[0]*1.02+0.01,w/cells[1]*1.02+0.01),order=3)[:h,:w]
    u=np.argsort(np.argsort(n.ravel())).reshape(n.shape)/(n.size-1)         # rank -> uniform 0..1
    return u<np.clip(edge_distance(mask,pl,panel)/width,0,1)
def fade_field(mask,pl,panel,fade):
    """Per-pixel factor 0..1: 1 in the middle, falling linearly to 0 at the panel edge over the last `fade` mm. None if no fade."""
    if not fade: return None
    return np.clip(edge_distance(mask,pl,panel)/fade,0,1).astype(np.float32)
def ink_mask(fname,crop,erase=(),rotate=0):
    g=Image.open(IMG+fname).convert("L")
    if rotate: g=g.rotate(rotate,expand=True,fillcolor=255)      # anticlockwise, before the crop; crop boxes are in the turned image
    if crop: g=g.crop(crop)
    a=np.asarray(g,dtype=np.float32); ink=np.clip((170-a)/80,0,1)      # 1 = black line, 0 = paper/watermark
    for x1,y1,x2,y2 in erase: ink[y1:y2,x1:x2]=0
    rows=np.where(ink.max(1)>0.5)[0]; cols=np.where(ink.max(0)>0.5)[0]
    pad=4; return ink[max(rows[0]-pad,0):rows[-1]+pad+1, max(cols[0]-pad,0):cols[-1]+pad+1]
def placement(mask,panel=None):
    """Rectangle (y0,y1,z0,z1) in box frame that the mask fills, aspect kept, centred in the panel."""
    panel=panel or PANEL; h,w=mask.shape; (y0,y1),(z0,z1)=panel['y'],panel['z']; W,H=y1-y0,z1-z0
    s=min(W/w,H/h); w_mm,h_mm=w*s,h*s; cy,cz=(y0+y1)/2,(z0+z1)/2
    return (cy-w_mm/2,cy+w_mm/2,cz-h_mm/2,cz+h_mm/2)
def render(parts,fname,azim=180,elev=0,size=900,ss=3,center=None,radius=None,light=(-0.7,-0.3,0.65),fill=0.92,up=None,art=None):
    W=H=size*ss; az,el=np.radians(azim),np.radians(elev)
    view=np.array([np.cos(el)*np.cos(az),np.cos(el)*np.sin(az),np.sin(el)])
    if up is None: right=np.cross([0,0,1.0],view); right/=np.linalg.norm(right); cup=np.cross(view,right)
    else: cup=np.array(up,float); cup-=view*(cup@view); cup/=np.linalg.norm(cup); right=np.cross(cup,view)
    allv=np.vstack([p[0].vertices for p in parts])
    if center is None: center=(allv.max(0)+allv.min(0))/2
    if radius is None: p=(allv-center)@np.stack([right,cup],1); radius=np.abs(p).max()/fill
    zbuf=np.full((H,W),-np.inf); img=np.zeros((H,W,4),dtype=np.float32)
    onback=np.zeros((H,W),bool); wy=np.zeros((H,W),np.float32); wz=np.zeros((H,W),np.float32)
    L=np.array(light,float); L/=np.linalg.norm(L); scale=(W/2)/radius
    for part in parts:
        m,base=part[0],np.array(part[1],float); isbody=len(part)>2 and part[2]
        V=(m.vertices-center); u=V@right*scale+W/2; v=H/2-V@cup*scale; d=V@view
        n=m.face_normals; lam=np.clip(n@L,0,1); spec=np.clip(n@view,0,1)**8*0.08
        k=np.ones(len(m.faces))
        if len(part)>3 and part[3] is not None:                      # darken the floor of a recess so it reads in flat shading
            kk=part[3](m); k=k*kk if kk.dtype!=bool else np.where(kk,0.62,1.0)   # a float array is a per-face factor (e.g. by depth)
        cols=np.clip((base[None,:]*(0.42+0.58*lam[:,None])+spec[:,None])*k[:,None],0,1); F=m.faces
        back=isbody and ((n[:,0]<-0.99)&(np.abs(m.triangles_center[:,0]-BACK_X)<0.05))
        Yv,Zv=m.vertices[:,1],m.vertices[:,2]
        for fi in np.where((n@view)>0)[0]:
            i0,i1,i2=F[fi]; x0,y0,x1,y1,x2,y2=u[i0],v[i0],u[i1],v[i1],u[i2],v[i2]
            xmin=int(max(np.floor(min(x0,x1,x2)),0)); xmax=int(min(np.ceil(max(x0,x1,x2)),W-1))
            ymin=int(max(np.floor(min(y0,y1,y2)),0)); ymax=int(min(np.ceil(max(y0,y1,y2)),H-1))
            if xmax<xmin or ymax<ymin: continue
            det=(x1-x0)*(y2-y0)-(x2-x0)*(y1-y0)
            if abs(det)<1e-12: continue
            X,Y=np.meshgrid(np.arange(xmin,xmax+1)+0.5,np.arange(ymin,ymax+1)+0.5)
            w1=((X-x0)*(y2-y0)-(x2-x0)*(Y-y0))/det; w2=((x1-x0)*(Y-y0)-(X-x0)*(y1-y0))/det; w0=1-w1-w2
            inside=(w0>=-1e-6)&(w1>=-1e-6)&(w2>=-1e-6)
            if not inside.any(): continue
            depth=w0*d[i0]+w1*d[i1]+w2*d[i2]; sub=zbuf[ymin:ymax+1,xmin:xmax+1]; upd=inside&(depth>sub)
            sub[upd]=depth[upd]; img[ymin:ymax+1,xmin:xmax+1][upd]=np.append(cols[fi],1.0)
            fb=onback[ymin:ymax+1,xmin:xmax+1]; fb[upd]=bool(isbody) and bool(back[fi])
            if isbody and back[fi]:
                wy[ymin:ymax+1,xmin:xmax+1][upd]=(w0*Yv[i0]+w1*Yv[i1]+w2*Yv[i2])[upd]
                wz[ymin:ymax+1,xmin:xmax+1][upd]=(w0*Zv[i0]+w1*Zv[i1]+w2*Zv[i2])[upd]
    if art is not None:
        mask,(ay0,ay1,az0,az1)=art[:2]; fade=art[2] if len(art)>2 else None; h,w=mask.shape
        if fade is not None: mask=mask*fade
        sel=onback&(wy>=ay0)&(wy<=ay1)&(wz>=az0)&(wz<=az1)
        # seen from behind, screen-right is -Y, so image column 0 sits at +Y (ay1)
        cx=np.clip(((ay1-wy[sel])/(ay1-ay0)*w).astype(int),0,w-1); cy=np.clip(((az1-wz[sel])/(az1-az0)*h).astype(int),0,h-1)
        k=1-0.65*mask[cy,cx]; img[sel,:3]*=k[:,None]
    out=img.reshape(size,ss,size,ss,4).mean(axis=(1,3)); a=out[...,3:4]; rgb=np.where(a>0,out[...,:3]/np.maximum(a,1e-6),0)
    Image.fromarray((np.clip(np.concatenate([rgb,a],-1),0,1)*255).astype(np.uint8),"RGBA").save(OUT+fname); return fname
BODY=(0.60,0.62,0.66); LID=(0.33,0.46,0.74); PIN=(0.25,0.65,0.35)
PARTS=[(body,BODY,True),(lid,LID),(pin,PIN)]
def job(i):
    label,fname,crop,erase,panel,rot,fade,drop,prune=spec(i); mask=ink_mask(fname,crop,erase,rot); pl=placement(mask,panel)
    for keep in (dropout_keep(mask,pl,panel,drop),prune_keep(mask,pl,panel,prune)):
        if keep is not None: mask=mask*keep
    art=(mask,pl,fade_field(mask,pl,panel,fade))
    a=render(PARTS,f"{label}_back.png",azim=180,elev=0,center=np.array([0,0,50.0]),radius=54,art=art)
    b=render(PARTS,f"{label}_back_iso.png",azim=140,elev=22,light=(-0.6,0.3,0.75),art=art)
    return label,a,b,mask.shape,placement(mask,panel)
def contact(results):
    tile=450; cols=5; rows=(len(results)+cols-1)//cols; sheet=Image.new("RGB",(cols*tile,rows*(tile+40)),(245,245,247)); d=ImageDraw.Draw(sheet)
    try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",22)
    except Exception: font=ImageFont.load_default()
    for i,(label,a,b,shape,pl) in enumerate(results):
        im=Image.open(OUT+a).convert("RGBA").resize((tile,tile),Image.LANCZOS); bg=Image.new("RGBA",im.size,(245,245,247,255)); bg.alpha_composite(im)
        x,y=(i%cols)*tile,(i//cols)*(tile+40); sheet.paste(bg.convert("RGB"),(x,y))
        d.text((x+12,y+tile+8),label[3:].replace("_"," ")+f"  {pl[1]-pl[0]:.0f} x {pl[3]-pl[2]:.0f} mm",fill=(40,40,40),font=font)
    sheet.save(OUT+"00_contact_sheet.png")
if __name__=="__main__":
    os.makedirs(OUT,exist_ok=True)
    sel=[int(a)-1 for a in sys.argv[2:]] if sys.argv[2:] else range(len(DESIGNS))
    with ProcessPoolExecutor(max_workers=8) as ex: results=list(ex.map(job,sel))
    for r in results: print("saved",r[0],"mask",r[3],"placed %.1f..%.1f x %.1f..%.1f mm"%r[4],flush=True)
    if len(results)==len(DESIGNS): contact(results)
