import HttpClient from "app/common/api/http-client";
import { createChartDataFromObject } from "app/common/functions/helper";
import { ObjectWithUnknownFields } from "app/common/types/http.types";
import { FilterFieldBase } from "app/modules/filters/field/field-type";

export default class QaMetricsApi {
	static baseUrl = "qa_metrics";

	public static async getCount(): Promise<any> {
		try {
			return await HttpClient.get(`${this.baseUrl}/`);
		} catch (e) {
			throw e;
		}
	}

	public static async getFilters(): Promise<any> {
		try {
			return await HttpClient.get(`${this.baseUrl}/filter/`);
		} catch (e) {
			throw e;
		}
	}

	public static async saveFilters(filters: FilterFieldBase[]): Promise<any> {
		try {
			return await HttpClient.post(`${this.baseUrl}/filter/`, undefined, { filters });
		} catch (e) {
			throw e;
		}
	}

	public static async getQAMetricsData() {
		try {
			const res = await HttpClient.get(`${this.baseUrl}/predictions_info/`);

			res.ttr_chart = createChartDataFromObject(res.ttr_chart);
			res.priority_chart = createChartDataFromObject(res.priority_chart);
			res.resolution_chart = Object.entries(res.resolution_chart).map(([name, data]) => {
				return {
					name,
					data: createChartDataFromObject(data as ObjectWithUnknownFields<number>),
				};
			});

			return res;
		} catch (e) {
			throw e;
		}
	}

	public static async getQAMetricsPredictionsTable(limit: number, offset: number) {
		try {
			return await HttpClient.post(`${this.baseUrl}/predictions_table/`, undefined, {
				limit,
				offset,
			});
		} catch (e) {
			throw e;
		}
	}
}
