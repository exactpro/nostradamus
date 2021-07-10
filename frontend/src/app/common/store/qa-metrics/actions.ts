import {
	QAMetricsAllData, QAMetricsPrioritySortBy,
	QAMetricsRecordsCount, QAMetricsStatuses
} from "app/common/store/qa-metrics/types";
import { ObjectWithUnknownFields } from "app/common/types/http.types";
import { FilterFieldBase } from "app/modules/filters/field/field-type";
import { getFieldEmptyValue, setFieldValue } from "app/modules/filters/field/field.helper-function";

export const setQaMetricsStatuses = (statuses: Partial<QAMetricsStatuses>) =>
	({
		type: "SET_QA_METRICS_PAGE_STATUS",
		statuses
	} as const);

export const setQaMetricsRecordsCount = (records_count: QAMetricsRecordsCount) =>
	({
		type: "SET_QA_METRICS_RECORDS_COUNT",
		records_count,
	} as const);

export const setQaMetricsFilter = (fields: FilterFieldBase[]) =>
	({
		type: "SET_QA_METRICS_FILTER",
		fields: // cause api don't return "current_value" property for unfilled field
			fields.map((field: FilterFieldBase) => ({
				exact_match: false,
				current_value: setFieldValue(
					field.type,
					field.current_value || getFieldEmptyValue(field.type)
				),
				...field,
			}))
	} as const);


export const setQAMetricsAllData = (data: QAMetricsAllData) =>
	({
		type: "SET_QA_METRICS_ALL_DATA",
		data,
	} as const);

export const setQAMetricsTable = (tableData: ObjectWithUnknownFields[]) =>
	({
		type: "SET_QA_METRICS_PAGE_TABLE",
		tableData,
	} as const);

export const changeQAMetricsPrioritySortBy = (sortBy: QAMetricsPrioritySortBy) =>
	({
		sortBy,
		type: "CHANGE_SORT_BY_QA_METRICS_PRIORITY",
	} as const);

export const clearQAMetricsData = () =>
	({
		type: "CLEAR_QA_METRICS_DATA",
	} as const);
