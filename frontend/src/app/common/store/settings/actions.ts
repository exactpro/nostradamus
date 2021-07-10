import {
	SettingsActionTypes,
	SettingsSections,
	SettingsDataUnion,
	FilterData,
	PredictionTableData,
	SettingsStatuses,
} from "app/common/store/settings/types";

export const activateSettings = () =>
	({
		type: SettingsActionTypes.activateSettings,
	} as const);

export const setSettingsStatus = (statuses: Partial<SettingsStatuses>) =>
	({
		statuses,
		type: SettingsActionTypes.setSettingsStatus,
	} as const);

export const uploadData = (section: SettingsSections, settings: SettingsDataUnion) =>
	({
		section,
		settings,
		type: SettingsActionTypes.uploadData,
	} as const);

export const setATFiltersDefaultData = (filtersData: FilterData[]) => ({
	filtersData,
	type: SettingsActionTypes.setATFiltersDefaultData
} as const)

export const setQAMetricsFiltersDefaultData = (filtersData: FilterData[]) => ({
	filtersData,
	type: SettingsActionTypes.setQAMetricsFiltersDefaultData
} as const)

export const setPredictionsDefaultData = (predictionData: PredictionTableData[]) => ({
	predictionData,
	type: SettingsActionTypes.setPredictionsDefaultData
} as const)

export const setCollectingDataStatus = (isCollectionFinished: boolean) =>
	({
		isCollectionFinished,
		type: SettingsActionTypes.setCollectingDataStatus,
	} as const);

export const clearSettings = () =>
	({
		type: SettingsActionTypes.clearSettings,
	} as const);
