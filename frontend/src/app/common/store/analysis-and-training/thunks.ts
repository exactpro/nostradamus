import { AnalysisAndTrainingApi } from 'app/common/api/analysis-and-training.api';
import {
	changeStatus,
	setAnalysisAndTrainingStatistic,
	setDefectSubmission,
	setIsCollectingFinish,
	updateFrequentlyTerms,
} from 'app/common/store/analysis-and-training/actions';
import { HttpError, HttpStatus } from 'app/common/types/http.types';
import { FilterFieldBase } from 'app/modules/filters/field/field-type';
import { checkFieldIsFilled } from 'app/modules/filters/field/field.helper-function';
import { setMainStatistic } from 'app/modules/main-statistic/store';
import { initSignificantTermsStore, setStatusLoadingState } from 'app/modules/significant-terms/store/actions';
import { addToast } from 'app/modules/toasts-overlay/store/actions';
import { ToastStyle } from 'app/modules/toasts-overlay/store/types';

export const getDashboardData = () => {
	return async (dispatch: any) => {
		dispatch(changeStatus(HttpStatus.LOADING));

		try {
			let res = await AnalysisAndTrainingApi.getAnalysisAndTrainingData();

			// if response is empty, issue loading process is set to in progress state
			if (Object.values(res).length) {
				if (res.records_count.filtered) {

					// TODO: to be refactored
					if(res.filters){
						res.filters.forEach((item: any, index: number)=>item.current_value=[]);
					}

					if (Array.isArray(res.frequently_terms)) {
						dispatch(updateFrequentlyTerms(res.frequently_terms));
					}

					dispatch(setAnalysisAndTrainingStatistic(res.statistics));

					if (res.significant_terms.chosen_metric) {
						dispatch(initSignificantTermsStore(res.significant_terms));
					}

					dispatch(changeStatus(HttpStatus.FINISHED));
				} else {
					dispatch(changeStatus(HttpStatus.FAILED));
					dispatch(addToast('With cached filters we didn\'t find data. Try to change filter.', ToastStyle.Warning));
				}

        if (res.records_count) {
					res.records_count.filtered = res.records_count.total;
					dispatch(setMainStatistic(res.records_count));
				}

				return res.filters;
			} else {
				dispatch(changeStatus(HttpStatus.PREVIEW));
				dispatch(setIsCollectingFinish(false));
				dispatch(addToast('Data is collecting...', ToastStyle.Warning))
			}
		} catch (e) {
			dispatch(changeStatus(HttpStatus.FAILED));

			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
		}
	};
};

export const applyAnalysisAndTrainingFilters = (filters: FilterFieldBase[]) => {
	return async (dispatch: any) => {

		dispatch(changeStatus(HttpStatus.LOADING));

		try {
			let res = await AnalysisAndTrainingApi.sendFilters({
				action: filters.length ? 'apply' : 'Clear',
				// send fields which are filled in
				filters: [ ...filters.filter((field) => checkFieldIsFilled(field.filtration_type, field.current_value)) ]
			});

			if (Object.values(res).length) {
				dispatch(setMainStatistic(res.records_count));
				dispatch(updateFrequentlyTerms(res.frequently_terms));
				dispatch(setAnalysisAndTrainingStatistic(res.statistics))

				if (res.significant_terms.chosen_metric) {
					dispatch(initSignificantTermsStore(res.significant_terms));
				}
				else {
					dispatch(setStatusLoadingState(HttpStatus.FAILED));
				}

				dispatch(changeStatus(HttpStatus.FINISHED));
				return res.filters;
			} else {
				dispatch(addToast('Data cannot be found. Please change filters.', ToastStyle.Warning));
				dispatch(changeStatus(HttpStatus.FAILED));
				return filters;
			}
		} catch (e) {
			dispatch(changeStatus(HttpStatus.PREVIEW));
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
		}
	};
};

export const updateDefectSubmission = (period: string) => {
	return async (dispatch: any) => {

		try {
			let res = await AnalysisAndTrainingApi.defectSubmission(period);
			dispatch(setDefectSubmission(res.submission_chart));
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
		}
	};
};
