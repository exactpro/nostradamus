import { QAMetricsStore } from 'app/common/store/qa-metrics/types';
import { InferValueTypes } from 'app/common/store/utils';
import { HttpStatus } from 'app/common/types/http.types'; 
import * as actions from './actions'; 
import { fixTTRBarChartAxisDisplayStyle, fixTTRPredictionTableDisplayStyle } from 'app/common/functions/helper';

const initialState: QAMetricsStore = {
	statuses: {
		filters: HttpStatus.PREVIEW,
		data: HttpStatus.PREVIEW,
		table: HttpStatus.PREVIEW,
	},
	records_count: {
		total: 0,
		filtered: 0
	},
	isModelTrained: true,
	predictions_table: [],
	prediction_table_rows_count: 0,
	areas_of_testing_chart: {},
	priority_chart: {},
	ttr_chart: {},
	resolution_chart: {},
};

type actionsQAMetricsTypes = ReturnType<InferValueTypes<typeof actions>>;

export const qaMetricsPageReducer = (state: QAMetricsStore = initialState, action: actionsQAMetricsTypes): QAMetricsStore => {
	switch (action.type) {

		case 'SET_QA_METRICS_PAGE_STATUS':
			return {
				...state,
				statuses: {
					...state.statuses,
					[action.part]: action.newStatus,
				},
			};

		case 'SET_STATUS_TRAIN_MODEL_QA_METRICS':
			return {
				...state,
				isModelTrained: action.newModelStatus
			};

		case 'SET_QA_METRICS_RECORDS_COUNT':
			return {
				...state,
				records_count: { ...action.records_count }
			};

		case 'SET_QA_METRICS_ALL_DATA': 
			return {
				...state,
				predictions_table: [...fixTTRPredictionTableDisplayStyle(action.data.predictions_table)],
				prediction_table_rows_count: action.data.prediction_table_rows_count,
				areas_of_testing_chart: { ...action.data.areas_of_testing_chart },
				priority_chart: { ...action.data.priority_chart },
				ttr_chart: { ...fixTTRBarChartAxisDisplayStyle(action.data.ttr_chart) },
				resolution_chart: { ...action.data.resolution_chart },
			};

		case 'SET_QA_METRICS_PAGE_TABLE':
			return {
				...state,
				predictions_table: [...fixTTRPredictionTableDisplayStyle(action.tableData)],
			};

		case "CLEAR_QA_METRICS_DATA":
			return {...initialState};

		default:
			return state;
	}
};

