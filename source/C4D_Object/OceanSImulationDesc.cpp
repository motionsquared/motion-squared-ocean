//
//  Created by Manuel MAGALHAES on 14/01/13.
//  Copyright (c) 2013 Valkaari. All rights reserved.
//
//  Modified by Kent Barber on 29 /07/22.
//  Copyright (c) 2022 GameLogicDesign Limited.All rights reserved.
//

#include "c4d.h"
#include "c4d_symbols.h"
#include "description/OceanDescription.h"
#include "main.h"

cinema::Bool RegisterOceanSimulationDescription()
{
	return cinema::RegisterDescription(MS_OCEAN_DESCRIPTION_ID, "OceanDescription"_s);
}
