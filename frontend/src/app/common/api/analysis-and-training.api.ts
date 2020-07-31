import { HttpClient } from 'app/common/api/http-client';
import { AnalysisAndTrainingStatistic, ApplyFilterBody } from 'app/common/types/analysis-and-training.types';
import store from 'app/common/store/configureStore';
import { FilterFieldBase } from 'app/modules/filters/field/field-type';
import { MainStatisticData } from 'app/modules/main-statistic/main-statistic';
import { addToast } from 'app/modules/toasts-overlay/store/actions';
import { ToastStyle } from 'app/modules/toasts-overlay/store/types';

export class AnalysisAndTrainingApi {

	static baseUrl: string = 'analysis_and_training';

	public static async getTotalStatistic(): Promise<{records_count?: MainStatisticData}> {
		try {
			return await HttpClient.get(this.baseUrl + '/');
		} catch (e) {
			store.dispatch(addToast(e.detail, ToastStyle.Error))
			throw e;
		}
	}

	public static async getFilter(): Promise<FilterFieldBase[]> {
		try {
			return await HttpClient.get(this.baseUrl + '/filter/');
		} catch (e) {
			store.dispatch(addToast(e.detail, ToastStyle.Error))
			throw e;
		}
	}

	public static async saveFilter(filterBody: ApplyFilterBody) {
		try {
			return await HttpClient.post(this.baseUrl + '/filter/', {}, { ...filterBody });
		} catch (e) {
			store.dispatch(addToast(e.detail, ToastStyle.Error))
			throw e;
		}
	}

	public static async getFrequentlyTerms() {
		try {
			return await HttpClient.get(this.baseUrl + '/frequently_terms/');
		} catch (e) {
			store.dispatch(addToast(e.detail, ToastStyle.Error))
			throw e;
		}
	}

	public static async getStatistic(): Promise<AnalysisAndTrainingStatistic> {
		try {
			let request = await HttpClient.get(this.baseUrl + '/statistics/');
			return request.statistics;
		} catch (e) {
			store.dispatch(addToast(e.detail, ToastStyle.Error))
			throw e;
		}
	}

	public static async getDefectSubmission(timeFilter?: string) {
		try {
			if (timeFilter) {
				return await HttpClient.post(this.baseUrl + '/defect_submission/', { period: timeFilter });
			} else {
				return await HttpClient.get(this.baseUrl + '/defect_submission/');
			}
		} catch (e) {
			throw e;
		}
	}

	public static async getSignificantTermsData() {
		try {
			return await HttpClient.get(this.baseUrl + '/significant_terms/');
		} catch (e) {
			throw e;
		}
	}

	public static async getSignificantTermsList(metric: string) {
		try {
			return await HttpClient.post(this.baseUrl + '/significant_terms/', { metric });
		} catch (e) {
			throw e;
		}
	}

	public static async trainModel() {
		try {
			return await HttpClient.post(this.baseUrl + '/train/', {});
		} catch (e) {
			throw e;
		}
	}

}
