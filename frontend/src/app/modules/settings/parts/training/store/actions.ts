import { SettingsStatuses } from "app/common/store/settings/types";
import {
	SettingsTrainingResponseType,
	SettingsTrainingSendEntitiesAndResolution,
	SettingsTrainingSendSourceField,
	TrainingActionTypes,
	TrainingSubSection,
} from "app/modules/settings/parts/training/store/types";

export const setSettingsTrainingData = (
	data: SettingsTrainingResponseType,
	section: TrainingSubSection
) =>
	({
		data,
		section,
		type: TrainingActionTypes.setSettingsTrainingData,
	} as const);

export const setSettingsTrainingStatus = (statuses: Partial<SettingsStatuses>) =>
	({
		statuses,
		type: TrainingActionTypes.setSettingsTrainingStatus,
	} as const);

export const clearSettingsTrainingData = () =>
	({ type: TrainingActionTypes.clearSettingsTrainingData } as const);

export const updateDefaultEntitiesAndResolutionData = (data: SettingsTrainingSendEntitiesAndResolution) =>
	({
		data,
		type: TrainingActionTypes.updateDefaultEntitiesAndResolutionData
	} as const)

export const updateDefaultSourceField = ({ source_field }: SettingsTrainingSendSourceField) =>
	({
		source_field,
		type: TrainingActionTypes.updateDefaultSourceField
	} as const)