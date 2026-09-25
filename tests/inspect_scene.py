"""Run with Cinema 4D c4dpy. Read-only scene inventory; never saves the input."""
import c4d
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
report = {'stage': 'started', 'c4d_version': c4d.GetC4DVersion()}
output = OUT / os.environ.get('MS_OCEAN_REPORT', 'scene-inventory.json')

def flush():
    output.write_text(json.dumps(report, indent=2), encoding='utf-8')

def walk(obj):
    while obj:
        yield obj
        yield from walk(obj.GetDown())
        obj = obj.GetNext()

flush()
try:
    report['pre_s24_probes']={str(i):c4d.plugins.FindPlugin(i,c4d.PLUGINTYPE_ANY) is not None for i in (1026624,1026641)}
    scene = Path(os.environ.get('MS_OCEAN_SCENE', str(ROOT / 'fixtures' / 'legacy-scene.c4d')))
    doc = c4d.documents.LoadDocument(str(scene), c4d.SCENEFILTER_OBJECTS | c4d.SCENEFILTER_MATERIALS)
    if doc is None:
        raise RuntimeError('LoadDocument failed')
    report['stage'] = 'loaded'
    report['fps'] = doc.GetFps()
    report['objects'] = []
    report['tags']=[]
    for obj in walk(doc.GetFirstObject()):
        item = {'name': obj.GetName(), 'type': obj.GetType()}
        if obj.GetType() in (1026624,1051458,1051489,1057479,1057480,1000001,1000002) or 'ocean' in obj.GetName().lower() or 'hot' in obj.GetName().lower():
            item['parameters'] = {str(i):repr(obj[i]) for i in range(10000,10029)}
            if obj.GetType()==1026624:
                item['old_parameters']={str(i):repr(obj[i]) for i in range(1000,1022)}
            item['tracks'] = []
            track = obj.GetFirstCTrack()
            while track:
                item['tracks'].append(str(track.GetDescriptionID()))
                track = track.GetNext()
            item['registered'] = c4d.plugins.FindPlugin(obj.GetType(), c4d.PLUGINTYPE_OBJECT) is not None
        report['objects'].append(item)
        for tag in obj.GetTags():
            entry={'object':obj.GetName(),'name':tag.GetName(),'type':tag.GetType()}
            entry['container']=[{'id':key,'value':repr(value)} for key,value in tag.GetDataInstance()]
            report['tags'].append(entry)
    report['shaders']=[]
    mat=doc.GetFirstMaterial()
    while mat:
        for shader in walk(mat.GetFirstShader()):
            item={'material':mat.GetName(),'name':shader.GetName(),'type':shader.GetType()}
            if shader.GetType()==1026641:
                item['parameters']={str(i):repr(shader[i]) for i in range(1000,1019)}
            report['shaders'].append(item)
        mat=mat.GetNext()
    report['stage'] = 'complete'
except BaseException as exc:
    report['error'] = repr(exc)
finally:
    flush()
