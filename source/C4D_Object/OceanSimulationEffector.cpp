// Cinema 4D ocean port: Manuel Magalhaes / Valkaari (2010-2013).
// Copyright 2022 GameLogicDesign Limited. Kent Barber's HOT4D baseline.
// C4D 2026 API adaptation incorporates work from Aitidi/HOT4D-C4D2026Plus.
// Motion Squared modifications (2026): compatibility, masks, undo and build integration.
// Distributed under GNU GPL v2; see LICENSE.txt and THIRD-PARTY-NOTICES.md.

#include "c4d.h"
#include "main.h"
#include "c4d_symbols.h"
#include "c4d_baseeffectorplugin.h"

#include "description/OceanDescription.h"
#include "OceanSimulation/OceanSimulation_decl.h"

#include "OceanSimulationEffector.h"

Bool OceanSimulationEffector::GetDEnabling(const GeListNode* node, const DescID& id, const GeData& t_data, DESCFLAGS_ENABLE flags, const BaseContainer* itemdesc) const
{
	if (id[0].id == OD_CURRENTTIME)
	{
		// current Time have to be disable if auto anim is on
		GeData data;
		node->GetParameter(CreateDescID(OD_AUTO_ANIM_TIME), data, DESCFLAGS_GET::NONE);
		return !data.GetBool();
	}

	return SUPER::GetDEnabling(node, id, t_data, flags, itemdesc);

}

// Int32 	OceanSimulationEffector::GetEffectorFlags()
// {
//
//	// don't work as i want =)
//	return  EFFECTORFLAGS_TIMEDEPENDENT;
// }

EXECUTIONRESULT 	OceanSimulationEffector::Execute(BaseObject *op, BaseDocument *doc, BaseThread *bt, Int32 priority, EXECUTIONFLAGS flags)
{

	if (priority != EXECUTIONPRIORITY_EXPRESSION)
		return EXECUTIONRESULT::OK;

	maxon::Bool doAutoTime;

	GeData							uiData;
	op->GetParameter(CreateDescID(OD_AUTO_ANIM_TIME), uiData, DESCFLAGS_GET::NONE);
	doAutoTime = uiData.GetBool();

	if (doAutoTime)
	{
		BaseTime btCurrentTime;
		maxon::Float    currentFrame;
		btCurrentTime = doc->GetTime();
		currentFrame = (maxon::Float)btCurrentTime.GetFrame(doc->GetFps());
		if (currentTime_ != currentFrame)
		{
			currentTime_ = currentFrame;
			op->SetDirty(DIRTYFLAGS::DATA);
		}
	}

	return EXECUTIONRESULT::OK;

}

Bool OceanSimulationEffector::InitEffector(GeListNode* node, Bool isCloneInit)
{

	BaseObject		*op = (BaseObject*)node;
	if (!op)
		return false;

	BaseContainer *bc = op->GetDataInstance();
	if (!bc)
		return false;

	if (!isCloneInit)
	{
		op->SetParameter(CreateDescID(OD_OCEAN_RESOLUTION), GeData(7), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_SEED), GeData(12345), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_OCEAN_SIZE), GeData(400.0), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_WIND_SPEED), GeData(20.0), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_WIND_DIRECTION), GeData(120.0), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_SHRT_WAVELENGHT), GeData(0.01), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_WAVE_HEIGHT), GeData(30.0), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_CHOPAMOUNT), GeData(0.5), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_DAMP_REFLECT), GeData(1.0), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_WIND_ALIGNMENT), GeData(1.0), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_OCEAN_DEPTH), GeData(200.0), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_CURRENTTIME), GeData(0.0), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_TIMELOOP), GeData(90), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_TIMESCALE), GeData(0.5), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_AUTO_ANIM_TIME), GeData(true), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_DO_CATMU_INTER), GeData(false), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_DO_JACOBIAN), GeData(false), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_DO_CHOPYNESS), GeData(true), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_PSEL_THRES), GeData(0.1), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_JACOB_THRES), GeData(0.5), DESCFLAGS_SET::NONE);
		op->SetParameter(CreateDescID(OD_FOAM_THRES), GeData(0.03), DESCFLAGS_SET::NONE);

		bc->SetFloat(ID_MG_BASEEFFECTOR_MINSTRENGTH, -1.0);
		bc->SetBool(ID_MG_BASEEFFECTOR_POSITION_ACTIVE, true);
		bc->SetVector(ID_MG_BASEEFFECTOR_POSITION, Vector(50.0));
	}

	iferr_scope_handler{
		err.DiagOutput();

		return false;
	};

	if (oceanSimulationRef_ == nullptr)
	{

		oceanSimulationRef_ = OceanSimulation::Ocean().Create() iferr_return;
	}

	return true;
}

maxon::Result<maxon::GenericData> OceanSimulationEffector::InitPoints(const BaseObject* op, const BaseObject* gen, const BaseDocument* doc, const EffectorDataStruct& data, MoData* md, BaseThread* thread) const
{

	iferr_scope;

	const BaseContainer* bc = op->GetDataInstance();
	if (!bc)
		return maxon::GenericData();

	if (oceanSimulationRef_ == nullptr)
	{
		oceanSimulationRef_ = OceanSimulation::Ocean().Create() iferr_return;
	}

	maxon::Float					oceanSize, windSpeed, windDirection, shrtWaveLenght, waveHeight, chopAmount, dampReflection, windAlign, oceanDepth, timeScale;
	maxon::Int32					oceanResolution, seed, timeLoop;
	maxon::Bool						doChopyness, doAutoTime;

	GeData							uiData;
	op->GetParameter(CreateDescID(OD_OCEAN_RESOLUTION), uiData, DESCFLAGS_GET::NONE);
	oceanResolution = 1 << uiData.GetInt32();

	op->GetParameter(CreateDescID(OD_OCEAN_SIZE), uiData, DESCFLAGS_GET::NONE);
	oceanSize = uiData.GetFloat();

	op->GetParameter(CreateDescID(OD_SHRT_WAVELENGHT), uiData, DESCFLAGS_GET::NONE);
	shrtWaveLenght = uiData.GetFloat();

	op->GetParameter(CreateDescID(OD_WAVE_HEIGHT), uiData, DESCFLAGS_GET::NONE);
	waveHeight = uiData.GetFloat();

	op->GetParameter(CreateDescID(OD_WIND_SPEED), uiData, DESCFLAGS_GET::NONE);
	windSpeed = uiData.GetFloat();

	op->GetParameter(CreateDescID(OD_WIND_DIRECTION), uiData, DESCFLAGS_GET::NONE);
	windDirection = DegToRad(uiData.GetFloat());

	op->GetParameter(CreateDescID(OD_WIND_ALIGNMENT), uiData, DESCFLAGS_GET::NONE);
	windAlign = uiData.GetFloat();

	op->GetParameter(CreateDescID(OD_DAMP_REFLECT), uiData, DESCFLAGS_GET::NONE);
	dampReflection = uiData.GetFloat();

	op->GetParameter(CreateDescID(OD_SEED), uiData, DESCFLAGS_GET::NONE);
	seed = uiData.GetInt32();

	op->GetParameter(CreateDescID(OD_OCEAN_DEPTH), uiData, DESCFLAGS_GET::NONE);
	oceanDepth = uiData.GetFloat();

	op->GetParameter(CreateDescID(OD_CHOPAMOUNT), uiData, DESCFLAGS_GET::NONE);
	chopAmount = uiData.GetFloat();

	op->GetParameter(CreateDescID(OD_TIMELOOP), uiData, DESCFLAGS_GET::NONE);
	timeLoop = uiData.GetInt32();

	op->GetParameter(CreateDescID(OD_TIMESCALE), uiData, DESCFLAGS_GET::NONE);
	timeScale = uiData.GetFloat();

	op->GetParameter(CreateDescID(OD_AUTO_ANIM_TIME), uiData, DESCFLAGS_GET::NONE);
	doAutoTime = uiData.GetBool();

	if (doAutoTime) currentTime_ = doc->GetTime().GetFrame(doc->GetFps());
	if (!doAutoTime)
	{
		op->GetParameter(CreateDescID(OD_CURRENTTIME), uiData, DESCFLAGS_GET::NONE);
		currentTime_ = uiData.GetFloat();
	}

	op->GetParameter(CreateDescID(OD_DO_CHOPYNESS), uiData, DESCFLAGS_GET::NONE);
	doChopyness = uiData.GetBool();

	if (oceanSimulationRef_.NeedUpdate(oceanResolution, oceanSize, shrtWaveLenght, waveHeight, windSpeed, windDirection, windAlign, dampReflection, seed))
	{
		oceanSimulationRef_.Init(oceanResolution, oceanSize, shrtWaveLenght, waveHeight, windSpeed, windDirection, windAlign, dampReflection, seed) iferr_return;
	}

	oceanSimulationRef_.Animate(currentTime_, timeLoop, timeScale, oceanDepth, chopAmount, true, doChopyness, false, false) iferr_return;

	return maxon::GenericData();
}

maxon::Result<void> OceanSimulationEffector::EvaluatePoint(const BaseObject* op, const maxon::Vector p, maxon::Vector &displacement) const
{
	iferr_scope;

	maxon::Float waveHeight;
	maxon::Bool doCatmuInter;

	GeData							uiData;
	op->GetParameter(CreateDescID(OD_WAVE_HEIGHT), uiData, DESCFLAGS_GET::NONE);
	waveHeight = uiData.GetFloat();

	op->GetParameter(CreateDescID(OD_DO_CATMU_INTER), uiData, DESCFLAGS_GET::NONE);
	doCatmuInter = uiData.GetBool();

	OceanSimulation::INTERTYPE interType = OceanSimulation::INTERTYPE::LINEAR;
	if (doCatmuInter)
		interType = OceanSimulation::INTERTYPE::CATMULLROM;

	maxon::Vector normal;
	maxon::Float jMinus;
	oceanSimulationRef_.EvaluatePoint(interType, p, displacement, normal, jMinus) iferr_return;
	if (!CompareFloatTolerant(waveHeight, 0.0))
		displacement /= waveHeight; // scale down the result by the wavelegnth so the result should be beetween -1 and 1
	// jMinus /= waveHeight;
	return  maxon::OK;
}

void OceanSimulationEffector::CalcPointValue(const BaseObject* op, const BaseObject* gen, const BaseDocument* doc, const EffectorDataStruct& data, const maxon::GenericData& extraData, MutableEffectorDataStruct& mdata, Int32 index, MoData* md, const Vector& globalpos, Float fall_weight) const
{
	iferr_scope_handler
	{
		err.DbgStop();
		return;
	};
	maxon::Vector disp;

	EvaluatePoint(op, globalpos, disp) iferr_return;

	mdata._strengthValues.pos = disp;
	mdata._strengthValues.rot = disp;
	mdata._strengthValues.scale = disp;

}

Vector OceanSimulationEffector::CalcPointColor(const BaseObject* op, const BaseObject* gen, const BaseDocument* doc, const EffectorDataStruct& data, const maxon::GenericData& extraData, const MutableEffectorDataStruct& mdata, Int32 index, MoData* md, const Vector& globalpos, Float fall_weight) const
{
	iferr_scope_handler
	{
		err.DbgStop();
		return Vector(0);
	};
	maxon::Vector disp;

	EvaluatePoint(op, globalpos, disp) iferr_return;

	return disp;

}

Bool RegisterOceanSimulationEffector()
{
    if (!RegisterEffectorPlugin(MS_OCEAN_EFFECTOR_ID, "Motion Squared Ocean Effector"_s,
        OBJECT_CALL_ADDEXECUTION, OceanSimulationEffector::Alloc,
        "OOceanEffector"_s, AutoBitmap("hot4D_eff.tif"_s), 0)) return false;
#ifdef MS_OCEAN_LEGACY_COMPAT
    for (Int32 id : {1051489, 1057480})
    {
        if (FindPlugin(id, PLUGINTYPE::ANY)) continue;
        if (!RegisterEffectorPlugin(id, "HOT4D Legacy Effector (Motion Squared)"_s,
            OBJECT_CALL_ADDEXECUTION | PLUGINFLAG_HIDE | PLUGINFLAG_HIDEPLUGINMENU,
            OceanSimulationEffector::Alloc, id == 1051489 ? "OOceanEffectorValkaari"_s : "OOceanEffectorKent"_s,
            AutoBitmap("hot4D_eff.tif"_s), 0)) return false;
    }
#endif
    return true;
}
