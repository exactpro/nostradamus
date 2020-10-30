import QaMetricsApi from "app/common/api/qa-metrics.api";
import {
	setQAMetricsAllData,
	setQaMetricsRecordsCount,
	setQaMetricsStatus,
	setQAMetricsTable,
	setStatusTrainModelQAMetrics,
} from "app/common/store/qa-metrics/actions";
import { HttpError, HttpStatus } from "app/common/types/http.types";
import { FilterFieldBase } from "app/modules/filters/field/field-type";
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";
import {
	checkFieldIsFilled,
	getFieldEmptyValue,
	setFieldValue,
} from "app/modules/filters/field/field.helper-function";
import { FiltersPopUp } from "app/modules/filters/filters";

export const initQAMetrics = () => {
	return async (dispatch: any) => {
		dispatch(setQaMetricsStatus("filters", HttpStatus.LOADING));

		let countsRes;
		let filtersRes;

		try {
			countsRes = await QaMetricsApi.getCount();
			filtersRes = await QaMetricsApi.getFilters();
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
			dispatch(setQaMetricsStatus("filters", HttpStatus.FAILED));
			return;
		}

		const recordsCountCode = countsRes.status;
		const filtersResCode = filtersRes.status;

		const recordsCountResBody = await countsRes.json();
		const filtersResBody = await filtersRes.json();

		dispatch(setQaMetricsStatus("filters", HttpStatus.FINISHED));

		if (recordsCountCode === 209 || filtersResCode === 209) {
			const warning = recordsCountResBody.warning || filtersResBody.warning;
			dispatch(setQaMetricsStatus("filters", HttpStatus.PREVIEW));
			dispatch(setStatusTrainModelQAMetrics(false));
			dispatch(addToast(warning.detail || warning.message, ToastStyle.Warning));
			return [];
		}

		if (!recordsCountResBody.records_count.filtered) {
			dispatch(setQaMetricsStatus("data", HttpStatus.FAILED));
		}

		dispatch(setQaMetricsRecordsCount(recordsCountResBody.records_count));
		dispatch(setStatusTrainModelQAMetrics(true));

		return filtersResBody.map((field: FilterFieldBase) => ({
			...field,
			exact_match: false,
			current_value: setFieldValue(
				field.filtration_type,
				field.current_value || getFieldEmptyValue(field.filtration_type)
			),
		}));
	};
};

export const saveQAMetricsFilters = (filters: FilterFieldBase[]) => {
	return async (dispatch: any) => {
		dispatch(setQaMetricsStatus("filters", HttpStatus.LOADING));

		let response;

		try {
			response = await QaMetricsApi.saveFilters([
				...filters.filter((field) =>
					checkFieldIsFilled(field.filtration_type, field.current_value)
				),
			]);
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
			dispatch(setQaMetricsStatus("filters", HttpStatus.FAILED));
			return;
		}

		const code = response.status;
		const body = await response.json();

		dispatch(setQaMetricsStatus("filters", HttpStatus.FINISHED));

		if (code === 209) {
			dispatch(setQaMetricsStatus("filters", HttpStatus.PREVIEW));
			dispatch(setStatusTrainModelQAMetrics(false));
			dispatch(addToast(body.warning.detail || body.warning.message, ToastStyle.Warning));
			return [];
		}

		if (body.warning) {
			dispatch(setQaMetricsStatus("filters", HttpStatus.PREVIEW));
			dispatch(setStatusTrainModelQAMetrics(false));
			return [];
		}

		// check, that bugs is founded
		if (!body.records_count.filtered) {
			dispatch(setQaMetricsStatus("data", HttpStatus.FAILED));
			dispatch(addToast(FiltersPopUp.noDataFound, ToastStyle.Warning));
		}

		dispatch(setStatusTrainModelQAMetrics(true));
		dispatch(setQaMetricsRecordsCount(body.records_count));

		const newFilters = body.filters.map((field: FilterFieldBase) => ({
			...field,
			exact_match: false,
			current_value: setFieldValue(
				field.filtration_type,
				getFieldEmptyValue(field.filtration_type)
			),
		}));

		return newFilters;
	};
};

export const updateQAMetricsData = () => {
	return async (dispatch: any) => {
		dispatch(setQaMetricsStatus("data", HttpStatus.LOADING));

		// TODO: make try/catch block shortly
		try {
			// send request
			const response = await QaMetricsApi.getQAMetricsData();

			// separate to code and body
			const code = response.status;
			const body = await response.json();

			// check, everything is ok
			if (code === 209) {
				dispatch(setQaMetricsStatus("data", HttpStatus.PREVIEW));
				dispatch(setStatusTrainModelQAMetrics(false));
				dispatch(addToast(body.warning.detail || body.warning.message, ToastStyle.Error));
				return;
			}

			// save data to store
			dispatch(setQAMetricsAllData(body));
			dispatch(setQaMetricsStatus("data", HttpStatus.FINISHED));
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
			dispatch(setQaMetricsStatus("data", HttpStatus.FAILED));
		}
	};
};

export const updateQAMetricsTable = (limit: number, offset: number) => {
	return async (dispatch: any) => {
		dispatch(setQaMetricsStatus("table", HttpStatus.RELOADING));

		// TODO: make try/catch block shortly
		try {
			const response = await QaMetricsApi.getQAMetricsPredictionsTable(limit, offset);

			const code = response.status;
			const body = await response.json();

			// check, everything is ok
			if (code === 209) {
				dispatch(setQaMetricsStatus("table", HttpStatus.PREVIEW));
				dispatch(addToast(body.warning.detail || body.warning.message, ToastStyle.Error));
				return;
			}

			// save data to store
			dispatch(setQAMetricsTable(body));
			dispatch(setQaMetricsStatus("table", HttpStatus.FINISHED));
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
			dispatch(setQaMetricsStatus("table", HttpStatus.FAILED));
		}
	};
};
