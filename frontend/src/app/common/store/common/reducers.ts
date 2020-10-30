import { CommonStore } from "app/common/store/common/types";
import { InferValueTypes } from "app/common/store/utils";
import * as actions from "./actions";

const initialState: CommonStore = {
	isCollectingFinished: false,
	isTrainFinished: false,
};

type actionsUserTypes = ReturnType<InferValueTypes<typeof actions>>;

export const commonReducer = (state: CommonStore = initialState, action: actionsUserTypes) => {

	switch (action.type) {

		case 'MARK_LOAD_ISSUES_FINISHED':
			return {
				...state,
				isCollectingFinished: true,
			};

		default:
			return { ...state };
	}
};
