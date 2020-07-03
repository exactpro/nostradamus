import { HttpClient } from 'app/common/api/http-client';
import { ApplyFilterBody } from 'app/common/store/analysis-and-training/types';

export class AnalysisAndTrainingApi {

	static baseUrl: string = 'analysis_and_training';

	public static async getAnalysisAndTrainingData(): Promise<any> {
		try {
			return await HttpClient.get(this.baseUrl + '/');
		} catch (e) {
			throw e;
		}
	}

	public static async defectSubmission(timeFilter: string) {
		try {
			return await HttpClient.get(this.baseUrl + '/defect_submission/', { period: timeFilter });
		} catch (e) {
			throw e;
		}
	}

	public static async getTerms(metric: string) {
		try {
			return await HttpClient.get(this.baseUrl + '/significant_terms/', { metric });
		} catch (e) {
			throw e;
		}
	}

	public static async sendFilters(filterBody: ApplyFilterBody) {
		try {
			return await HttpClient.post(this.baseUrl + '/filter/', {}, { ...filterBody });
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
