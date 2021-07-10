import { getDataFromLocalStorage } from "app/common/functions/local-storage";
import { AuthStore } from "app/common/store/auth/types";
import { HttpStatus } from "app/common/types/http.types";
import { User } from "app/common/types/user.types";
import { InferValueTypes } from "app/common/store/utils";
import * as actions from "./actions";

const initialState: AuthStore = {
	status: HttpStatus.PREVIEW,
	user: getDataFromLocalStorage<User>("user"),
};

type actionsUserTypes = ReturnType<InferValueTypes<typeof actions>>;

export const authReducer = (state: AuthStore = initialState, action: actionsUserTypes) => {
	switch (action.type) {
		case "ACTION_AUTH_SET_USER":
			return {
				...state,
				user: action.user,
			};

		case "ACTION_AUTH_DELETE_USER":
			return {
				...state,
				user: null,
			};

		case "ACTION_AUTH_SET_STATUS":
			return {
				...state,
				status: action.status,
			};

		default:
			return state;
	}
};
