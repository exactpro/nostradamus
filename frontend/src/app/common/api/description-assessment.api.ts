import HttpClient from "app/common/api/http-client";
import { PredictMetric } from "app/modules/predict-text/predict-text";

export class DescriptionAssessmentApi {
	static baseUrl = "description_assessment";

	public static async getMetrics(): Promise<any> {
		try {
			return await HttpClient.get(`${this.baseUrl}/`);
		} catch (e) {
			throw e;
		}
	}

	public static async getHighlightedTerms(metric: PredictMetric) {
		try {
			return await HttpClient.post(`${this.baseUrl}/highlight/`, null, metric);
		} catch (e) {
			throw e;
		}
	}

	public static async predictText(text: string) {
		try {
			return await HttpClient.post(`${this.baseUrl}/predict/`, null, { description: text });
		} catch (e) {
			throw e;
		}
	}
}
