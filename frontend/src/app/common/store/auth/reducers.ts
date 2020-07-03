import { getDataFromLocalStorage } from 'app/common/functions/local-storage';
import { AuthStore } from 'app/common/store/auth/types';
import { HttpStatus } from 'app/common/types/http.types';
import { User } from 'app/common/types/user.types';
import * as actions from './actions';
import { InferValueTypes } from 'app/common/store/utils';

const initialState: AuthStore = {
	status: HttpStatus.PREVIEW,
	user: getDataFromLocalStorage<User>('user'),
	teamList: [],
};

type actionsUserTypes = ReturnType<InferValueTypes<typeof actions>>;

export const authReducer = (state: AuthStore = initialState, action: actionsUserTypes) => {

	switch (action.type) {

		case 'ACTION_AUTH_SET_USER':
			return {
				...state,
				user: action.user,
			};

		case 'ACTION_AUTH_DELETE_USER':
			return {
				...state,
				user: null,
			};

		case 'ACTION_AUTH_SET_STATUS':
			return {
				...state,
				status: action.status,
			};

		case 'ACTION_AUTH_SET_TEAM_LIST':
			return {
				...state,
				teamList: [...action.teamList],
			};

		default:
			return state;
	}
};
