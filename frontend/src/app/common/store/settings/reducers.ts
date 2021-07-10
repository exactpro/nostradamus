/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import { SettingsStore, SettingsActionTypes, SettingsData, SettingsStatuses } from "app/common/store/settings/types";
import { HttpStatus } from "app/common/types/http.types";
import { InferValueTypes } from "app/common/store/utils";
import { copyData } from "app/common/functions/helper";
import { combineReducers } from "redux";
import settingsTrainingReducer from "app/modules/settings/parts/training/store/reducer";
import * as actions from "app/common/store/settings/actions";

const initialState: SettingsStore = {
	isOpen: false,
	status: {
		filters: HttpStatus.PREVIEW,
		qa_metrics: HttpStatus.PREVIEW,
		predictions_table: HttpStatus.PREVIEW,
	},
	defaultSettings: {
		filters: {
			filter_settings: [],
			names: [],
		},
		qa_metrics: {
			filter_settings: [],
			names: [],
		},
		predictions_table: {
			predictions_table_settings: [],
			field_names: [],
		},
		training: {
			mark_up_source: "",
			mark_up_entities: [],
			bug_resolution: [
				{
					metric: "Resolution",
					value: "",
				},
				{
					metric: "Resolution",
					value: "",
				},
			],
		},
	},
};

type actionsUserTypes = ReturnType<InferValueTypes<typeof actions>>;

export const settingsReducer = (
	state: SettingsStore = initialState,
	action: actionsUserTypes
): SettingsStore => {
	const defaultSettings: SettingsData = { ...state.defaultSettings };
	const status: SettingsStatuses = { ...state.status };
	switch (action.type) {
		case SettingsActionTypes.activateSettings:
			return { ...state, isOpen: !state.isOpen };

		case SettingsActionTypes.setSettingsStatus:
			return {
				...state,
				status: {
					...status,
					...action.statuses
				}
			};

		case SettingsActionTypes.uploadData:
			defaultSettings[action.section] = copyData(action.settings);
			return { ...state, defaultSettings };

		case SettingsActionTypes.clearSettings:
			return { ...initialState };

		case SettingsActionTypes.setATFiltersDefaultData:
			defaultSettings.filters.filter_settings = copyData(action.filtersData);
			return { ...state, defaultSettings };

		case SettingsActionTypes.setQAMetricsFiltersDefaultData:
			defaultSettings.qa_metrics.filter_settings = copyData(action.filtersData);
			return { ...state, defaultSettings };

		case SettingsActionTypes.setPredictionsDefaultData:
			defaultSettings.predictions_table.predictions_table_settings = copyData(action.predictionData);
			return { ...state, defaultSettings };
		default:
			return { ...state };
	}
};

export const generalSettingsStore = combineReducers({
	settingsStore: settingsReducer,
	settingsTrainingStore: settingsTrainingReducer,
});
