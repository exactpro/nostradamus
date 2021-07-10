import { ChartData } from "app/common/components/charts/types";
import { QAMetricsPrioritySortBy, QAMetricsStore } from "app/common/store/qa-metrics/types";
import { InferValueTypes } from "app/common/store/utils";
import { HttpStatus } from "app/common/types/http.types";
import {
	fixTTRBarChartAxisDisplayStyle,
	fixTTRPredictionTableDisplayStyle
} from "app/common/functions/helper";
import * as actions from "./actions";

const initialState: QAMetricsStore = {
	filter: [],
	statuses: {
		filter: HttpStatus.PREVIEW,
		data: HttpStatus.PREVIEW,
		table: HttpStatus.PREVIEW,
	},
	records_count: {
		total: 0,
		filtered: 0,
	},
	predictions_table: [],
	prediction_table_rows_count: 0,
	areas_of_testing_chart: {},
	priority_chart: [],
	ttr_chart: [],
	resolution_chart: [],
};

type actionsTypes = ReturnType<InferValueTypes<typeof actions>>;

export const qaMetricsPageReducer = (
	state: QAMetricsStore = initialState,
	action: actionsTypes
): QAMetricsStore => {
	switch (action.type) {

		case "SET_QA_METRICS_PAGE_STATUS":
			return {
				...state,
				statuses: {
					...state.statuses,
					...action.statuses
				},
			};

		case "SET_QA_METRICS_RECORDS_COUNT":
			return {
				...state,
				records_count: { ...action.records_count },
			};

		case "SET_QA_METRICS_FILTER":
			return {
				...state,
				filter: [ ...action.fields ],
			};

		case "SET_QA_METRICS_ALL_DATA":
			return {
				...state,
				predictions_table: [...fixTTRPredictionTableDisplayStyle(action.data.predictions_table)],
				prediction_table_rows_count: action.data.prediction_table_rows_count,
				areas_of_testing_chart: { ...action.data.areas_of_testing_chart },
				priority_chart: [ ...sortPriority(action.data.priority_chart, QAMetricsPrioritySortBy.Value)],
				ttr_chart: [ ...fixTTRBarChartAxisDisplayStyle(action.data.ttr_chart) ],
				resolution_chart: [ ...action.data.resolution_chart ] ,
			};

		case "SET_QA_METRICS_PAGE_TABLE":
			return {
				...state,
				predictions_table: [...fixTTRPredictionTableDisplayStyle(action.tableData)],
			};

		case "CHANGE_SORT_BY_QA_METRICS_PRIORITY":
			return {
				...state,
				priority_chart: [ ...sortPriority(state.priority_chart, action.sortBy)],
			};

		case "CLEAR_QA_METRICS_DATA":
			return { ...initialState };

		default:
			return state;
	}
};

function sortPriority(
	chartData: ChartData,
	fieldName: QAMetricsPrioritySortBy
): ChartData {
	return chartData.sort((a, b) => {
		if (fieldName === QAMetricsPrioritySortBy.Value) {
			return a[fieldName] < b[fieldName] ? 1 : -1;
		}
		return a[fieldName] < b[fieldName] ? -1 : 1;
	})
}
