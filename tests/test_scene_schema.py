"""Regression contract for saved HOT4D parameter IDs; no Cinema 4D needed."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def enum_values(path):
    text = re.sub(r'//[^\n]*', '', path.read_text())
    body = text.split('enum', 1)[1].split('{', 1)[1].split('}', 1)[0]
    value = -1
    result = {}
    for entry in body.split(','):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split('=')
        value = int(parts[1].strip()) if len(parts) == 2 else value + 1
        result[parts[0].strip()] = value
    return result

class SavedSceneSchema(unittest.TestCase):
    def test_valkaari_and_kent_saved_parameter_contract(self):
        # Values from Valkaari S24 eb81a55 and Kent e46775b, not inferred from UI order.
        expected = {
            'OCEAN_RESOLUTION':10000, 'OCEAN_SIZE':10001, 'WIND_SPEED':10002,
            'WIND_DIRECTION':10003, 'SHRT_WAVELENGHT':10004, 'WAVE_HEIGHT':10005,
            'SEED':10006, 'CHOPAMOUNT':10007, 'DAMP_REFLECT':10008,
            'WIND_ALIGNMENT':10009, 'OCEAN_DEPTH':10010, 'CURRENTTIME':10011,
            'TIMELOOP':10012, 'TIMESCALE':10013, 'AUTO_ANIM_TIME':10014,
            'DO_CHOPYNESS':10015, 'DO_CATMU_INTER':10016, 'DO_NORMALS':10017,
            'DO_JACOBIAN':10018, 'JACOBMAP':10019, 'ID_GRP_FOAM':10020,
            'FOAMMAP':10021, 'PRE_RUN_FOAM':10022, 'JACOB_THRES':10023,
            'FOAM_THRES':10024, 'PSEL_PARTICLES':10025, 'PSEL_THRES':10026,
            'ACTIVE_DEFORM':10027,
        }
        actual = enum_values(ROOT/'res/description/OceanDescription.h')
        for key, value in expected.items():
            self.assertEqual(actual['OD_' + key], value, key)
        self.assertEqual(actual['OD_CREATE_FOAM_TAGS'],10028)

if __name__ == '__main__':
    unittest.main()
