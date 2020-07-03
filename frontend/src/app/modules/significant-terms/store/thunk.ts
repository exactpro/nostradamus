import { AnalysisAndTrainingApi } from 'app/common/api/analysis-and-training.api';
import { HttpError, HttpStatus } from 'app/common/types/http.types';
import { changeChosenMetric, setStatusLoadingState, setTerms } from 'app/modules/significant-terms/store/actions';
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";

export const updateTerms = (metric: string) => {
	return async (dispatch: any) => {
		dispatch(changeChosenMetric(metric));
		dispatch(setStatusLoadingState(HttpStatus.RELOADING));

		try {
			let res = await AnalysisAndTrainingApi.getTerms(metric);
			dispatch(setTerms(res.significant_terms));
			dispatch(setStatusLoadingState(HttpStatus.FINISHED));
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
			dispatch(setStatusLoadingState(HttpStatus.FAILED));
		}
	};
};
