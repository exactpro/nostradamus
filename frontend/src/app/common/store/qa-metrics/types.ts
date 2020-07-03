import { HttpStatus } from 'app/common/types/http.types';

export type QAMetricsStorePart = 'filters' | 'data' | 'table';

export interface QAMetricsStore {
	isModelTrained: boolean,
	statuses: {
		[key in QAMetricsStorePart]: HttpStatus
	},
	predictions_table: QAMetricsData[];
	prediction_table_rows_count: number;
	areas_of_testing_chart: QAMetricsData;
	priority_chart: QAMetricsData;
	ttr_chart: QAMetricsData;
	resolution_chart: QAMetricsResolutionChartData;
}

export interface QAMetricsData {
	[key: string]: unknown
}

export interface QAMetricsResolutionChartData {
	[key: string]: QAMetricsData
}
