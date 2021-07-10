import { AnalysisAndTrainingApi } from "app/common/api/analysis-and-training.api";
import {
	setCardStatuses, setCardWarnings,
	setDefectSubmission,
	setFilters,
	setFrequentlyTerms,
	setSignificantTerms,
	setStatistic,
	setTotalStatistic,
	updateSignificantTermsChosenMetric,
	updateSignificantTermsList
} from "app/common/store/analysis-and-training/actions";
import { checkIssuesExist } from "app/common/store/common/utils";
import {
	AnalysisAndTrainingStatistic,
	DefectSubmissionData,
	SignificantTermsData,
} from "app/common/types/analysis-and-training.types";
import { HttpStatus } from "app/common/types/http.types";
import { FilterFieldBase } from "app/modules/filters/field/field-type";
import { FiltersPopUp } from "app/modules/filters/filters";
import { MainStatisticData } from "app/modules/main-statistic/main-statistic";
import { Terms } from "app/modules/significant-terms/store/types";
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";

export const uploadDashboardData = () => {
	return async (dispatch: any) => {
		dispatch(
			setCardStatuses({
				filter: HttpStatus.LOADING,
				frequentlyTerms: HttpStatus.LOADING,
				defectSubmission: HttpStatus.LOADING,
				statistic: HttpStatus.LOADING,
				significantTerms: HttpStatus.LOADING,
			})
		);

		let totalStatistic: MainStatisticData;

		if (await checkIssuesExist()) {
			dispatch(uploadFilters());
			totalStatistic = await dispatch(uploadTotalStatistic());
		} else {
			dispatch(
				setCardStatuses({
					filter: HttpStatus.PREVIEW,
					frequentlyTerms: HttpStatus.PREVIEW,
					defectSubmission: HttpStatus.PREVIEW,
					statistic: HttpStatus.PREVIEW,
					significantTerms: HttpStatus.PREVIEW,
				})
			)
			return;
		}

		if (totalStatistic.filtered) {
			dispatch(uploadFrequentlyTerms());
			dispatch(uploadStatistic());
			dispatch(uploadDefectSubmission());
			dispatch(uploadSignificantTermsData());
		} else {
			dispatch(
				addToast(
					"With cached filters we didn't find data. Try to change filter.",
					ToastStyle.Warning
				)
			);

			dispatch(
				setCardStatuses({
					frequentlyTerms: HttpStatus.PREVIEW,
					defectSubmission: HttpStatus.PREVIEW,
					statistic: HttpStatus.PREVIEW,
					significantTerms: HttpStatus.PREVIEW,
				})
			)
		}
	};
};

export const uploadTotalStatistic = () => {
	return async (dispatch: any) => {

		let records_count: MainStatisticData;

		try {
			records_count = await AnalysisAndTrainingApi.getTotalStatistic();
		} catch (e) {
			// don't have loading status
			return;
		}

		dispatch(setTotalStatistic(records_count));

		return records_count;
	};
};

export const uploadFilters = () => {
	return async (dispatch: any) => {
		dispatch(
			setCardStatuses({
				filter: HttpStatus.LOADING,
			})
		);

		let filters: FilterFieldBase[];

		try {
			filters = await AnalysisAndTrainingApi.getFilter();
		} catch (e) {
			dispatch(
				setCardStatuses({
					filter: HttpStatus.FAILED,
				})
			);
			return;
		}

		dispatch(setFilters(filters));

		dispatch(
			setCardStatuses({
				filter: HttpStatus.FINISHED,
			})
		);
	};
};

export const updateFilters = (fields: FilterFieldBase[]) => {
	return async (dispatch: any) => {
		dispatch(
			setCardStatuses({
				filter: HttpStatus.LOADING,
				frequentlyTerms: HttpStatus.LOADING,
				defectSubmission: HttpStatus.LOADING,
				statistic: HttpStatus.LOADING,
				significantTerms: HttpStatus.LOADING,
			})
		);

		let response: {
			filters: FilterFieldBase[];
			records_count: MainStatisticData
		};

		try {
			response = await AnalysisAndTrainingApi.saveFilter({
				action: "apply",
				filters: [ ...fields ],
			});
		} catch (e) {
			dispatch(
				setCardStatuses({
					filter: HttpStatus.FAILED,
					frequentlyTerms: HttpStatus.FINISHED,
					defectSubmission: HttpStatus.FINISHED,
					statistic: HttpStatus.FINISHED,
					significantTerms: HttpStatus.FINISHED,
				})
			);
			return;
		}

		dispatch(setFilters(response.filters));
		dispatch(setTotalStatistic(response.records_count));

		dispatch(
			setCardStatuses({
				filter: HttpStatus.FINISHED,
			})
		);

		if (response.records_count.filtered) {
			dispatch(uploadFrequentlyTerms());
			dispatch(uploadStatistic());
			dispatch(uploadDefectSubmission());
			dispatch(uploadSignificantTermsData());
		} else {
			dispatch(addToast(FiltersPopUp.noDataFound, ToastStyle.Warning));

			dispatch(
				setCardStatuses({
					frequentlyTerms: HttpStatus.PREVIEW,
					defectSubmission: HttpStatus.PREVIEW,
					statistic: HttpStatus.PREVIEW,
					significantTerms: HttpStatus.PREVIEW,
				})
			);
		}
	};
};

export const uploadSignificantTermsData = () => {
	return async (dispatch: any) => {
		dispatch(
			setCardStatuses({
				significantTerms: HttpStatus.LOADING,
			})
		);

		let significant_terms: SignificantTermsData;

		try {
			significant_terms = await AnalysisAndTrainingApi.getSignificantTermsData();
		} catch (e) {
			dispatch(
				setCardWarnings({
					significantTerms: e.message,
				})
			);

			dispatch(
				setCardStatuses({
					significantTerms: HttpStatus.FAILED,
				})
			);

			return;
		}

		dispatch(setSignificantTerms(significant_terms));

		dispatch(
			setCardStatuses({
				significantTerms: HttpStatus.FINISHED,
			})
		);
	};
};

export const uploadSignificantTermsList = (metric: string) => {
	return async (dispatch: any) => {
		dispatch(
			setCardStatuses({
				significantTerms: HttpStatus.LOADING,
			})
		);

		dispatch(updateSignificantTermsChosenMetric(metric));

		let significant_terms: Terms;

		try {
			significant_terms = await AnalysisAndTrainingApi.getSignificantTermsList(metric);
		} catch (e) {
			dispatch(
				setCardWarnings({
					significantTerms: e.message,
				})
			);

			dispatch(
				setCardStatuses({
					significantTerms: HttpStatus.FAILED,
				})
			);
			return;
		}

		dispatch(updateSignificantTermsList(significant_terms));

		dispatch(
			setCardStatuses({
				significantTerms: HttpStatus.FINISHED,
			})
		);
	};
};

export const uploadDefectSubmission = (period?: string) => {
	return async (dispatch: any) => {
		dispatch(
			setCardStatuses({
				defectSubmission: HttpStatus.LOADING,
			})
		);

		let defectSubmission: DefectSubmissionData;

		try {
			defectSubmission = await AnalysisAndTrainingApi.getDefectSubmission(period);
		} catch (e) {
			dispatch(
				setCardStatuses({
					defectSubmission: HttpStatus.FAILED,
				})
			);
			return;
		}

		dispatch(setDefectSubmission(defectSubmission));
		dispatch(
			setCardStatuses({
				defectSubmission: HttpStatus.FINISHED,
			})
		);
	};
};

export const uploadFrequentlyTerms = () => {
	return async (dispatch: any) => {
		dispatch(
			setCardStatuses({
				frequentlyTerms: HttpStatus.LOADING,
			})
		);

		let frequentlyTerms: string[];

		try {
			frequentlyTerms = await AnalysisAndTrainingApi.getFrequentlyTerms();
		} catch (e) {
			dispatch(
				setCardWarnings({
					frequentlyTerms: e.message,
				})
			);

			dispatch(
				setCardStatuses({
					frequentlyTerms: HttpStatus.FAILED,
				})
			);
			return;
		}

		dispatch(setFrequentlyTerms(frequentlyTerms));

		dispatch(
			setCardStatuses({
				frequentlyTerms: HttpStatus.FINISHED,
			})
		);
	};
};

export const uploadStatistic = () => {
	return async (dispatch: any) => {
		dispatch(
			setCardStatuses({
				statistic: HttpStatus.LOADING,
			})
		);

		let statistic: AnalysisAndTrainingStatistic;

		try {
			statistic = await AnalysisAndTrainingApi.getStatistic();
		} catch (e) {
			dispatch(
				setCardStatuses({
					statistic: HttpStatus.FAILED,
				})
			);
			return;
		}

		dispatch(setStatistic(statistic));

		dispatch(
			setCardStatuses({
				statistic: HttpStatus.FINISHED,
			})
		);
	};
};
