import { HttpStatus } from "app/common/types/http.types";

export enum SettingsActionTypes {
	activateSettings = "ACTIVATE_SETTINGS",
	setSettingsStatus = "SET_SETTINGS_STATUS",
	uploadData = "UPLOAD_DATA",
	setData = "SET_DATA",
	clearData = "CLEAR_DATA",
	sendData = "SEND_DATA",
	setCollectingDataStatus = "SET_COLLECTING_DATA_STATUS",
	clearSettings = "CLEAR_SETTINGS",

	setATFiltersDefaultData = "SET_AT_FILTERS_DEFAULT_DATA",
	setQAMetricsFiltersDefaultData = "SET_QA_METRICS_FILTERS_DEFAULT_DATA",
	setPredictionsDefaultData = "SET_PREDICTIONS_DEFAULT_DATA",
}

export enum SettingsSections {
	filters = "filters",
	qaFilters = "qa_metrics",
	predictions = "predictions_table",
}

export type SettingsStatuses = {
	[key in SettingsSections]: HttpStatus
}

// Type for Filter section: Analysis&Training and QAMetrics
export type FilterData = {
	name: string;
	type: string;
};

export type FilterType = {
	filter_settings: FilterData[];
	names: string[];
};
// Type for PredictionTable section
export type PredictionTableData = {
	name: string;
	is_default: boolean;
	position: number;
	settings: number;
};

export type PredictionTableType = {
	predictions_table_settings: PredictionTableData[];
	field_names: string[];
};

// Type for Training section

export type MarkUpEntities = {
	area_of_testing: string;
	entities: string[];
};

export type BugResolution = {
	metric: string;
	value: string;
};

export type TrainingType = {
	mark_up_source: string;
	mark_up_entities: MarkUpEntities[];
	bug_resolution: BugResolution[];
};

export type SettingsDataUnion = FilterData[] | PredictionTableData[] | TrainingType;

export interface SettingsData {
	filters: FilterType;
	qa_metrics: FilterType;
	predictions_table: PredictionTableType;
	training: TrainingType;
}

export interface SettingsStore {
	isOpen: boolean; 
	status: SettingsStatuses;
	defaultSettings: SettingsData;
}

export interface SettingsResponseError {
	warning: {
		detail: string;
	};
}
