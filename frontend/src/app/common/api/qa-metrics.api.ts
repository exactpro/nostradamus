import { HttpClient } from 'app/common/api/http-client';
import { FilterFieldBase } from 'app/modules/filters/field/field-type';

export class QaMetricsApi {

	static baseUrl: string = 'qa_metrics';

	public static async getFilters(): Promise<any> {
		try {
			return await HttpClient.get(this.baseUrl + '/', undefined, undefined, true);
		} catch (e) {
			throw e;
		}
	}

	public static async getQAMetricsData(filters: FilterFieldBase[]) {
		try {
			return await HttpClient.post(this.baseUrl + '/predictions_info/', null, { filters }, undefined, true);
		} catch (e) {
			throw e;
		}
	}

	public static async getQAMetricsPredictionsTable(filters: FilterFieldBase[], limit: number, offset: number) {
		try {
			return await HttpClient.post(this.baseUrl + '/predictions_table/', null, { filters, limit, offset }, undefined, true);
		} catch (e) {
			throw e;
		}
	}
}
