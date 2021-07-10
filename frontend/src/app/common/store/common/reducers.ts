import { CommonStore } from "app/common/store/common/types";
import { InferValueTypes } from "app/common/store/utils";
import * as actions from "./actions";

const initialState: CommonStore = {
	isLoadedIssuesStatus: false,
	isIssuesExist: false,
	isSearchingModelFinished: false,
	isModelFounded: false,
};

type actionsUserTypes = ReturnType<InferValueTypes<typeof actions>>;

export const commonReducer = (state: CommonStore = initialState, action: actionsUserTypes) => {

	switch (action.type) {

		case 'UPDATE_COMMON_STATUSES':
			return {
				...state,
				...action.statuses,
			};

		case 'RESET_COMMON_STATUSES':
		return {
			...initialState
		};

		default:
			return { ...state };
	}
};
