import HttpClient from "app/common/api/http-client";
import {
	AnalysisAndTrainingStatistic,
	ApplyFilterBody,
} from "app/common/types/analysis-and-training.types";
import store from "app/common/store/configureStore";
import { FilterFieldBase } from "app/modules/filters/field/field-type";
import { MainStatisticData } from "app/modules/main-statistic/main-statistic";
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";

export class AnalysisAndTrainingApi {
	static baseUrl = "analysis_and_training";

	public static async getTotalStatistic(): Promise<MainStatisticData> {
		try {
			return await HttpClient.get(`${this.baseUrl}/`);
		} catch (e) {
			store.dispatch(addToast(e.detail, ToastStyle.Error));
			throw e;
		}
	}

	public static async getFilter(): Promise<FilterFieldBase[]> {
		try {
			return await HttpClient.get(`${this.baseUrl}/filter/`);
		} catch (e) {
			store.dispatch(addToast(e.detail, ToastStyle.Error));
			throw e;
		}
	}

	public static async saveFilter(filterBody: ApplyFilterBody) {
		try {
			return await HttpClient.post(`${this.baseUrl}/filter/`, {}, { ...filterBody });
		} catch (e) {
			store.dispatch(addToast(e.detail, ToastStyle.Error));
			throw e;
		}
	}

	public static async getFrequentlyTerms() {
		try {
			return await HttpClient.get(`${this.baseUrl}/frequently_terms/`);
		} catch (e) {
			throw e;
		}
	}

	public static async getStatistic(): Promise<AnalysisAndTrainingStatistic> {
		try {
			return  await HttpClient.get(`${this.baseUrl}/statistics/`);
		} catch (e) {
			store.dispatch(addToast(e.detail, ToastStyle.Error));
			throw e;
		}
	}

	public static async getDefectSubmission(timeFilter?: string) {
		try {
			return await HttpClient.get(
				`${this.baseUrl}/defect_submission/`,
				timeFilter ? { period: timeFilter } : undefined
			);
		} catch (e) {
			throw e;
		}
	}

	public static async getSignificantTermsData() {
		try {
			return await HttpClient.get(`${this.baseUrl}/significant_terms/`);
		} catch (e) {
			throw e;
		}
	}

	public static async getSignificantTermsList(metric: string) {
		try {
			return await HttpClient.post(`${this.baseUrl}/significant_terms/`, { metric });
		} catch (e) {
			throw e;
		}
	}

	public static async trainModel() {
		try {
			return await HttpClient.post(`ml-core/train/`, {});
		} catch (e) {
			throw e;
		}
	}


	public static async getCollectingDataStatus() {
		try {
			return await HttpClient.get(this.baseUrl + '/status/');
		} catch (e) {
			throw e;
		}
	}

	public static async getTrainingModelStatus() {
		try {
			await HttpClient.get('description_assessment/');
			return true;
		} catch (e) {
			return false
		}
	}

}
