#pragma once
#include "c4d.h"
#include "c4d_plugin.h"
#include <initializer_list>
// Development-only IDs. Obtain permanent Maxon IDs before public distribution.
#ifndef MS_OCEAN_DEFORMER_ID
#define MS_OCEAN_DEFORMER_ID 1000001
#endif
#ifndef MS_OCEAN_EFFECTOR_ID
#define MS_OCEAN_EFFECTOR_ID 1000002
#endif
#ifndef MS_OCEAN_DESCRIPTION_ID
#define MS_OCEAN_DESCRIPTION_ID 1000003
#endif
cinema::Bool RegisterOceanSimulationDescription();
cinema::Bool RegisterOceanSimulationDeformer();
cinema::Bool RegisterOceanSimulationEffector();
