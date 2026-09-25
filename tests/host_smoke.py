"""Cinema 4D host regression tests. Creates only test scenes in tests/results."""
import c4d
import json
import math
from c4d.modules import mograph
from pathlib import Path

OUT = Path(__file__).resolve().parent/'results'
OUT.mkdir(exist_ok=True)
report = {'stage':'started', 'tests':[]}

def flush():
    (OUT/'host-smoke.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

def check(label, condition):
    report['tests'].append({'name':label,'passed':bool(condition)})
    flush()
    if not condition:
        raise AssertionError(label)

def make_scene(type_id):
    doc=c4d.documents.BaseDocument()
    mesh=c4d.PolygonObject(9,4)
    mesh.SetAllPoints([c4d.Vector(x*30,0,z*30) for z in range(3) for x in range(3)])
    for k, (a,b,c,d) in enumerate([(0,1,4,3),(1,2,5,4),(3,4,7,6),(4,5,8,7)]):
        mesh.SetPolygon(k,c4d.CPolygon(a,b,c,d))
    mesh.Message(c4d.MSG_UPDATE)
    doc.InsertObject(mesh)
    ocean=c4d.BaseObject(type_id)
    if ocean is None:
        raise RuntimeError('Plugin type unavailable: '+str(type_id))
    ocean.InsertUnder(mesh)
    ocean.SetDeformMode(True)
    ocean[10000]=4
    ocean[10005]=17.5
    ocean[10006]=42
    ocean[10014]=False
    ocean[10011]=12.0
    return doc,mesh,ocean

def evaluate(doc,mesh):
    doc.ExecutePasses(None,True,True,True,c4d.BUILDFLAGS_NONE)
    cache=mesh.GetDeformCache()
    if cache is None:
        raise RuntimeError('No deformation cache')
    return [(p.x,p.y,p.z) for p in cache.GetAllPoints()]

flush()
try:
    outputs=[]
    documents=[]
    for type_id in (1000001,1051458,1057479):
        check('registered deformer '+str(type_id),c4d.plugins.FindPlugin(type_id,c4d.PLUGINTYPE_OBJECT) is not None)
        doc,mesh,ocean=make_scene(type_id)
        documents.append(doc)
        points=evaluate(doc,mesh)
        check('finite geometry '+str(type_id),all(math.isfinite(v) for p in points for v in p))
        check('nonzero waves '+str(type_id),any(abs(p[1])>1e-6 for p in points))
        outputs.append(points)
        clone=ocean.GetClone()
        check('clone settings '+str(type_id),clone[10005]==17.5 and clone[10006]==42)
        check('animatable description '+str(type_id),any(did[0].id==10005 for bc,did,gid in ocean.GetDescription(c4d.DESCFLAGS_DESC_NONE)))
        track=c4d.CTrack(ocean,c4d.DescID(c4d.DescLevel(10005,c4d.DTYPE_REAL,0)))
        ocean.InsertTrackSorted(track)
        key=track.GetCurve().AddKey(c4d.BaseTime(0))['key']
        key.SetValue(track.GetCurve(),17.5)
        dest=OUT/('roundtrip-'+str(type_id)+'.c4d')
        check('save '+str(type_id),c4d.documents.SaveDocument(doc,str(dest),c4d.SAVEDOCUMENTFLAGS_DONTADDTORECENTLIST,c4d.FORMAT_C4DEXPORT))
        loaded=c4d.documents.LoadDocument(str(dest),c4d.SCENEFILTER_OBJECTS)
        documents.append(loaded)
        restored=loaded.GetFirstObject().GetDown() if loaded else None
        check('roundtrip type and settings '+str(type_id),restored is not None and restored.GetType()==type_id and restored[10005]==17.5 and restored[10006]==42)
        check('roundtrip animation '+str(type_id),restored.GetFirstCTrack() is not None)
    check('legacy and modern numerical parity',outputs[0]==outputs[1]==outputs[2])
    doc,mesh,ocean=make_scene(1000001)
    original=[(p.x,p.y,p.z) for p in mesh.GetAllPoints()]
    mask=c4d.VariableTag(c4d.Tvertexmap,9)
    mask.SetName('Ocean test mask')
    mesh.InsertTag(mask)
    mask.SetAllHighlevelData([0.0]*9)
    restriction=c4d.BaseTag(c4d.Trestriction)
    ocean.InsertTag(restriction)
    restriction[c4d.RESTRICTIONTAG_NAME_01]=mask.GetName()
    check('zero vertex mask preserves geometry',evaluate(doc,mesh)==original)
    restriction.Remove()
    for loop,scale in ((0,0.5),(90,0.0)):
        ocean[10012]=loop
        ocean[10013]=scale
        ocean.SetDirty(c4d.DIRTYFLAGS_DATA)
        points=evaluate(doc,mesh)
        check('finite zero loop or speed '+str((loop,scale)),all(math.isfinite(v) for p in points for v in p))
    doc,mesh,ocean=make_scene(1000001)
    c4d.CallButton(ocean,10028)
    tags=[tag for tag in mesh.GetTags() if tag.GetType()==c4d.Tvertexcolor]
    check('foam button creates two linked tags',len(tags)==2 and ocean[10019] in tags and ocean[10021] in tags)
    c4d.CallButton(ocean,10028)
    check('foam button reuses existing tags',len([tag for tag in mesh.GetTags() if tag.GetType()==c4d.Tvertexcolor])==2)
    effector_outputs=[]
    for type_id in (1000002,1051489,1057480):
        doc=c4d.documents.BaseDocument()
        documents.append(doc)
        cloner=c4d.BaseObject(c4d.Omgcloner)
        doc.InsertObject(cloner)
        cloner[c4d.ID_MG_MOTIONGENERATOR_MODE]=c4d.ID_MG_MOTIONGENERATOR_MODE_LINEAR
        cloner[c4d.MG_LINEAR_COUNT]=3
        cloner[c4d.MG_LINEAR_OBJECT_POSITION]=c4d.Vector(30,0,0)
        c4d.BaseObject(c4d.Ocube).InsertUnder(cloner)
        effector=c4d.BaseObject(type_id)
        doc.InsertObject(effector)
        effector[10000]=4
        effector[10014]=False
        effector[10011]=12.0
        effectors=c4d.InExcludeData()
        effectors.InsertObject(effector,1)
        cloner[c4d.ID_MG_MOTIONGENERATOR_EFFECTORLIST]=effectors
        doc.ExecutePasses(None,True,True,True,c4d.BUILDFLAGS_NONE)
        data=mograph.GeGetMoData(cloner)
        check('MoGraph data '+str(type_id),data is not None)
        points=[(m.off.x,m.off.y,m.off.z) for m in data.GetArray(c4d.MODATA_MATRIX)]
        check('effector finite waves '+str(type_id),all(math.isfinite(v) for p in points for v in p) and any(abs(p[1])>1e-6 for p in points))
        effector_outputs.append(points)
    check('legacy and modern effector parity',effector_outputs[0]==effector_outputs[1]==effector_outputs[2])
    report['stage']='complete'
except BaseException as exc:
    report['stage']='failed'
    report['error']=repr(exc)
finally:
    flush()
