import HttpClient from "app/common/api/http-client";
import { createChartDataFromObject } from "app/common/functions/helper";
import { ObjectWithUnknownFields } from "app/common/types/http.types";
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
			const res = await HttpClient.post(`${this.baseUrl}/predict/`, null, { description: text });

			res["Time to Resolve"] = createChartDataFromObject(
				res["Time to Resolve"]
			);
			res.Priority = createChartDataFromObject(res.Priority);
			res.resolution = Object.entries(res.resolution).map(
				([name, data]) => {
					return {
						name,
						data: createChartDataFromObject(data as ObjectWithUnknownFields<number>),
					};
				}
			);

			return res;
		} catch (e) {
			throw e;
		}
	}
}
