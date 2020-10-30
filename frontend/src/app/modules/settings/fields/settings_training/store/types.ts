// Api training routs

import { HttpStatus } from "app/common/types/http.types";

export enum TrainingSubSection {
	markup_entities = "markup_entities",
	source_field = "source_field",
	bug_resolution = "bug_resolution",
}

// Action types
export enum TrainingActionTypes {
	setSettingsTrainingData = "SET_SETTINGS_TRAINING_DATA",
	setSettingsTrainingStatus = "SET_SETTINGS_TRAINING_STATUS",
	clearSettingsTrainingData = "CLEAR_SETTINGS_TRAINING_DATA",
}

// Source Field data type

export interface SourceFieldData {
	source_field: string;
	source_field_names: string[];
}

// Mark Up Entities data type

export interface MarkUpEntitiesElement {
	area_of_testing: string;
	entities: string[];
}

export interface MarkUpEntitiesData {
	mark_up_entities: MarkUpEntitiesElement[];
	entity_names: string[];
}

// Bug Resolution data type

export interface BugResolutionElement {
	metric: string;
	value: string;
}

export interface BugResolutionData {
	resolution_settings: BugResolutionElement[];
	resolution_names: string[];
}

// Training status type

export interface TrainingStatus {
	source_field: HttpStatus;
	bug_resolution: HttpStatus;
	markup_entities: HttpStatus;
}

// Training state type

export interface SettingTrainingStore {
	[key: string]: TrainingStatus | SourceFieldData | BugResolutionData | MarkUpEntitiesData;
	status: TrainingStatus;
	source_field: SourceFieldData;
	bug_resolution: BugResolutionData;
	markup_entities: MarkUpEntitiesData;
}

export type SettingsTrainingResponseType = SourceFieldData | BugResolutionData | MarkUpEntitiesData;

export interface SettingsTrainingResponseError {
	warning: string;
}
