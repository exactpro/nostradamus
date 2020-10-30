import {
	QAMetricsData,
	QAMetricsResolutionChartData,
	QAMetricsStorePart,
	QAMetricsRecordsCount,
} from "app/common/store/qa-metrics/types";
import { HttpStatus } from "app/common/types/http.types";

export interface QAMetricsAllData {
	predictions_table: QAMetricsData[];
	prediction_table_rows_count: number;
	areas_of_testing_chart: QAMetricsData;
	priority_chart: QAMetricsData;
	ttr_chart: QAMetricsData;
	resolution_chart: QAMetricsResolutionChartData;
}

export const setStatusTrainModelQAMetrics = (newModelStatus: boolean) =>
	({
		type: "SET_STATUS_TRAIN_MODEL_QA_METRICS",
		newModelStatus,
	} as const);

export const setQaMetricsStatus = (part: QAMetricsStorePart, newStatus: HttpStatus) =>
	({
		type: "SET_QA_METRICS_PAGE_STATUS",
		newStatus,
		part,
	} as const);

export const setQaMetricsRecordsCount = (records_count: QAMetricsRecordsCount) =>
	({
		type: "SET_QA_METRICS_RECORDS_COUNT",
		records_count,
	} as const);

export const setQAMetricsAllData = (data: QAMetricsAllData) =>
	({
		type: "SET_QA_METRICS_ALL_DATA",
		data,
	} as const);

export const setQAMetricsTable = (tableData: QAMetricsData[]) =>
	({
		type: "SET_QA_METRICS_PAGE_TABLE",
		tableData,
	} as const);

export const clearQAMetricsData = () =>
	({
		type: "CLEAR_QA_METRICS_DATA",
	} as const);
