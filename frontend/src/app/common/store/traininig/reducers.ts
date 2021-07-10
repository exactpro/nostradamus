import { TrainingStore } from "app/common/store/traininig/types";
import { InferValueTypes } from "app/common/store/utils";
import { HttpStatus } from "app/common/types/http.types";
import * as actions from "./actions";

const initialState: TrainingStore = {
	status: HttpStatus.LOADING,
};

type actionsTypes = ReturnType<InferValueTypes<typeof actions>>;

export const trainingReducers = (
	state: TrainingStore = initialState,
	action: actionsTypes
): TrainingStore => {
	switch (action.type) {
		case "SET_TRAINING_STATUS":
			return {
				...state,
				status: action.status,
			};

		default:
			return { ...state };
	}
};
