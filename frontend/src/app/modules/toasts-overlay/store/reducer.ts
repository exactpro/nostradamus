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

			if(!!state.toastList.find((item)=>{
				if(item.message===action.toast.message && item.style===action.toast.style){
					if(action.toast.outerId) item.outerId = action.toast.outerId;
					return true;
				}
				return false;
			})) return {...state};
			
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

		case 'TOASTS_REMOVE_TOAST_BY_OUTER_ID':
			return {
				...state,
				toastList: state.toastList.filter(toast => toast.outerId !== action.toastId)
			};

		default:
			return state;
	}
}
