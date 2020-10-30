/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import {
	TrainingActionTypes,
	SettingTrainingStore,
} from "app/modules/settings/fields/settings_training/store/types";
import { InferValueTypes } from "app/common/store/utils";
import { HttpStatus } from "app/common/types/http.types";

import * as actions from "app/modules/settings/fields/settings_training/store/actions";

const initialState: SettingTrainingStore = {
	status: {
		source_field: HttpStatus.PREVIEW,
		bug_resolution: HttpStatus.PREVIEW,
		markup_entities: HttpStatus.PREVIEW,
	},
	source_field: {
		source_field: "",
		source_field_names: [],
	},
	bug_resolution: {
		resolution_settings: [],
		resolution_names: [],
	},
	markup_entities: {
		mark_up_entities: [],
		entity_names: [],
	},
};
type actionsSettingsTrainingTypes = ReturnType<InferValueTypes<typeof actions>>;

export default function settingsTrainingReducer(
	state: SettingTrainingStore = initialState,
	action: actionsSettingsTrainingTypes
): SettingTrainingStore {
	const status = { ...state.status };

	switch (action.type) {
		case TrainingActionTypes.setSettingsTrainingData:
			if (!Object.keys(action.data).length) return { ...state };
			return { ...state, [action.section]: action.data };

		case TrainingActionTypes.setSettingsTrainingStatus:
			status[action.section] = action.status;
			return { ...state, status };

		case TrainingActionTypes.clearSettingsTrainingData:
			return { ...initialState };

		default:
			return { ...state };
	}
}
