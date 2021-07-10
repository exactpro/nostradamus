import { ChartData, ChartsList } from "app/common/components/charts/types";
import { HttpStatus, ObjectWithUnknownFields } from "app/common/types/http.types";
import { FilterFieldBase } from "app/modules/filters/field/field-type";
import { Terms } from "app/modules/significant-terms/store/types";

export interface QAMetricsStatuses {
	filter: HttpStatus;
	data: HttpStatus;
	table: HttpStatus;
}

export interface QAMetricsRecordsCount {
	total: number;
	filtered: number;
}

export enum QAMetricsPrioritySortBy {
	Value = 'value',
	Name = 'name'
}

export interface QAMetricsAllData {
	predictions_table: ObjectWithUnknownFields[];
	prediction_table_rows_count: number;
	areas_of_testing_chart: Terms;
	priority_chart: ChartData;
	ttr_chart: ChartData;
	resolution_chart: ChartsList;
}

export interface QAMetricsStore extends QAMetricsAllData {
	filter: FilterFieldBase[];
	statuses: QAMetricsStatuses;
	records_count: QAMetricsRecordsCount;
}

