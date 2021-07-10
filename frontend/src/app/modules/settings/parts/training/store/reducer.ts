/* eslint-disable @typescript-eslint/no-unsafe-assignment */
import {
	TrainingActionTypes,
	SettingTrainingStore,
} from "app/modules/settings/parts/training/store/types";
import { InferValueTypes } from "app/common/store/utils";
import { HttpStatus } from "app/common/types/http.types";

import * as actions from "app/modules/settings/parts/training/store/actions";
import { copyData, deepCopyData } from "app/common/functions/helper";

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
			return { ...state, [action.section]: copyData(action.data) };

		case TrainingActionTypes.setSettingsTrainingStatus:
			return {
				...state, status: {
					...status,
					...action.statuses
				}
			};

		case TrainingActionTypes.clearSettingsTrainingData:
			return { ...initialState };

		case TrainingActionTypes.updateDefaultEntitiesAndResolutionData:
			const { bug_resolution, markup_entities } = state;
			bug_resolution.resolution_settings = deepCopyData(action.data.bug_resolution);
			markup_entities.mark_up_entities = deepCopyData(action.data.mark_up_entities);
			return { ...state, bug_resolution, markup_entities };

		case TrainingActionTypes.updateDefaultSourceField:
			const { source_field } = state;
			source_field.source_field = action.source_field;
			return { ...state, source_field };

		default:
			return { ...state };
	}
}
