import { InferValueTypes } from 'app/common/store/utils';
import { HttpStatus } from 'app/common/types/http.types';
import { SignificantTermsState } from 'app/modules/significant-terms/store/types';
import * as actions from './actions';

const initialState: SignificantTermsState = {
	status: HttpStatus.PREVIEW,
	metrics: [],
	chosen_metric: null,
	terms: {}
};

type significantTermStoreActionsType = ReturnType<InferValueTypes<typeof actions>>;

function significantTerms(state: SignificantTermsState = initialState, action: significantTermStoreActionsType) {
	switch (action.type) {
		case 'SIGNIFICANT_TERMS_STORE_INIT':
			action.state.metrics.sort();
			return {
				...action.state,
			};

		case 'SIGNIFICANT_TERMS_CHANGE_CHOSEN_METRIC':
			return {
				...state,
				chosen_metric: action.metric,
			};

		case 'SIGNIFICANT_TERMS_SET_TERMS':
			return {
				...state,
				terms: {...action.terms} ,
			};

		case 'SIGNIFICANT_TERMS_SET_LOADING_STATUS':
			return {
				...state,
				status: action.status,
			};

		default:
			return state;
	}
}

export default significantTerms;
