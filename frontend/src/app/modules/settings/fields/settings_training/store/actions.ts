import { HttpStatus } from "app/common/types/http.types";
import {
	SettingsTrainingResponseType,
	TrainingActionTypes,
	TrainingSubSection,
} from "app/modules/settings/fields/settings_training/store/types";

export const setSettingsTrainingData = (
	data: SettingsTrainingResponseType,
	section: TrainingSubSection
) =>
	({
		data,
		section,
		type: TrainingActionTypes.setSettingsTrainingData,
	} as const);

export const setSettingsTrainingStatus = (status: HttpStatus, section: TrainingSubSection) =>
	({
		section,
		status,
		type: TrainingActionTypes.setSettingsTrainingStatus,
	} as const);

export const clearSettingsTrainingData = () =>
	({ type: TrainingActionTypes.clearSettingsTrainingData } as const);
