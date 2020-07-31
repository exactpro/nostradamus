import { QaMetricsApi } from 'app/common/api/qa-metrics.api';
import {
	setQAMetricsAllData,
	setQaMetricsStatus,
	setQAMetricsTable, 
	setStatusTrainModelQAMetrics,
} from 'app/common/store/qa-metrics/actions';
import { HttpError, HttpStatus } from 'app/common/types/http.types';
import { FilterFieldBase } from 'app/modules/filters/field/field-type';
import { addToast } from 'app/modules/toasts-overlay/store/actions';
import { ToastStyle } from 'app/modules/toasts-overlay/store/types';
import {
	checkFieldIsFilled,
	getFieldEmptyValue,
	setFieldValue,
} from 'app/modules/filters/field/field.helper-function';

export const updateQAMetricsFilters = () => {
	return async (dispatch: any) => {
		dispatch(setQaMetricsStatus('filters', HttpStatus.LOADING));

		try {
			let response = await QaMetricsApi.getFilters();
			let code = response.status;
			let body = await response.json();

			dispatch(setQaMetricsStatus('filters', HttpStatus.FINISHED));

			if (code === 209) {
				dispatch(setQaMetricsStatus('filters', HttpStatus.PREVIEW));
				dispatch(setStatusTrainModelQAMetrics(false));
				dispatch(addToast(body.warning.detail || body.warning.message, ToastStyle.Warning));
				return []
			}

			if (body.warning) {
				dispatch(setQaMetricsStatus('filters', HttpStatus.PREVIEW));
				dispatch(setStatusTrainModelQAMetrics(false));
				return []
			}

			dispatch(setStatusTrainModelQAMetrics(true));

			return body.map((field: FilterFieldBase) => ({
				...field,
				exact_match: false,
				current_value: setFieldValue(field.filtration_type, getFieldEmptyValue(field.filtration_type))
			}));
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
			dispatch(setQaMetricsStatus('filters', HttpStatus.FAILED));
		}
	};
};

export const updateQAMetricsData = (filters: FilterFieldBase[]) => {
	return async (dispatch: any) => {
		dispatch(setQaMetricsStatus('data', HttpStatus.LOADING));

		try {
			let response = await QaMetricsApi.getQAMetricsData(
				[...filters.filter((field) => checkFieldIsFilled(field.filtration_type, field.current_value))],
			);
			let code = response.status;
			let body = await response.json();
			if(!body.records_count.filtered) {
				dispatch(setQaMetricsStatus('data', HttpStatus.FINISHED));
				dispatch(addToast("Data isn't found. Try to change filter", ToastStyle.Warning));
				return;
			}
			
			if (code === 209) {
				dispatch(setQaMetricsStatus('data', HttpStatus.PREVIEW));
				dispatch(setStatusTrainModelQAMetrics(false));
				dispatch(addToast(body.warning.detail || body.warning.message, ToastStyle.Error));
				return;
			}

			if (Object.values(body).length) {
				dispatch(setQAMetricsAllData(body));
				dispatch(setQaMetricsStatus('data', HttpStatus.FINISHED));
			} else {
				dispatch(addToast('Data cannot be found. Please change filters.', ToastStyle.Warning));
				dispatch(setQaMetricsStatus('data', HttpStatus.PREVIEW));
			}
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
			dispatch(setQaMetricsStatus('data', HttpStatus.FAILED));
		}
	};
};

export const updateQAMetricsTable = (filters: FilterFieldBase[], limit: number, offset: number) => {
	return async (dispatch: any) => {
		dispatch(setQaMetricsStatus('table', HttpStatus.RELOADING));

		try {
			let response = await QaMetricsApi.getQAMetricsPredictionsTable(
				[...filters.filter((field) => checkFieldIsFilled(field.filtration_type, field.current_value))],
				limit, offset);
			let code = response.status;
			let body = await response.json();

			if (code === 209) {
				dispatch(setQaMetricsStatus('table', HttpStatus.PREVIEW));
				dispatch(setStatusTrainModelQAMetrics(false));
				dispatch(addToast(body.warning.detail || body.warning.message, ToastStyle.Error));
				return;
			}

			dispatch(setQAMetricsTable(body));
			dispatch(setQaMetricsStatus('table', HttpStatus.FINISHED));
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
			dispatch(setQaMetricsStatus('table', HttpStatus.FAILED));
		}
	};
};

