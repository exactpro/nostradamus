import HttpClient from "app/common/api/http-client";
import { FilterFieldBase } from "app/modules/filters/field/field-type";

export default class QaMetricsApi {
	static baseUrl = "qa_metrics";

	public static async getCount(): Promise<any> {
		try {
			return await HttpClient.get(`${this.baseUrl}/`, undefined, undefined, true);
		} catch (e) {
			throw e;
		}
	}

	public static async getFilters(): Promise<any> {
		try {
			return await HttpClient.get(`${this.baseUrl}/filter/`, undefined, undefined, true);
		} catch (e) {
			throw e;
		}
	}

	public static async saveFilters(filters: FilterFieldBase[]): Promise<any> {
		try {
			return await HttpClient.post(
				`${this.baseUrl}/filter/`,
				undefined,
				{ filters },
				undefined,
				true
			);
		} catch (e) {
			throw e;
		}
	}

	public static async getQAMetricsData() {
		try {
			return await HttpClient.get(`${this.baseUrl}/predictions_info/`, undefined, undefined, true);
		} catch (e) {
			throw e;
		}
	}

	public static async getQAMetricsPredictionsTable(limit: number, offset: number) {
		try {
			return await HttpClient.post(
				`${this.baseUrl}/predictions_table/`,
				undefined,
				{ limit, offset },
				undefined,
				true
			);
		} catch (e) {
			throw e;
		}
	}
}
