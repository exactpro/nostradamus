import { HttpStatus } from 'app/common/types/http.types';
import {
	SignificantTermsStateInitial,
	Terms,
} from 'app/modules/significant-terms/store/types';

export const initSignificantTermsStore = (state: SignificantTermsStateInitial) => ({
	type: 'SIGNIFICANT_TERMS_STORE_INIT',
	state: {
		...state,
		status: HttpStatus.FINISHED,
		terms: state.terms,
	},
} as const);

export const changeChosenMetric = (metric: string) => ({
	type: 'SIGNIFICANT_TERMS_CHANGE_CHOSEN_METRIC',
	metric,
} as const);

export const setTerms = (terms: Terms) => ({
	type: 'SIGNIFICANT_TERMS_SET_TERMS',
	terms,
} as const);

export const setStatusLoadingState = (status: HttpStatus) => ({
	type: 'SIGNIFICANT_TERMS_SET_LOADING_STATUS',
	status,
} as const);
