import { InferValueTypes } from 'app/common/store/utils';
import * as actions from './actions';
import { ToastStore } from 'app/modules/toasts-overlay/store/types';

const initialState: ToastStore = {
	newToastId: 0,
	toastList: [],
};

type toastsTermStoreActionsType = ReturnType<InferValueTypes<typeof actions>>;

export const toastsReducers = (state: ToastStore = initialState, action: toastsTermStoreActionsType) => {
	switch (action.type) {
		case 'TOASTS_ADD_TOAST':
			if(!!state.toastList.find((item)=>item.message===action.toast.message && item.style===action.toast.style)) return {...state}
		 	return {
				...state,
				newToastId: ++state.newToastId,
				toastList: [{
					id: state.newToastId,
					...action.toast
				}, ...state.toastList]
			};

		case 'TOASTS_REMOVE_TOAST':
			return {
				...state,
				toastList: state.toastList.filter(toast => toast.id !== action.toastId)
			};

		default:
			return state;
	}
}
