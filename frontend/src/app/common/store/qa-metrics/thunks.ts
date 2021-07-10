import QaMetricsApi from "app/common/api/qa-metrics.api";
import { checkModelIsFound } from "app/common/store/common/utils";
import {
	setQAMetricsAllData,
	setQaMetricsFilter,
	setQaMetricsRecordsCount,
	setQaMetricsStatuses,
	setQAMetricsTable,
} from "app/common/store/qa-metrics/actions";
import {
	QAMetricsRecordsCount,
	QAMetricsAllData
} from "app/common/store/qa-metrics/types";
import { HttpError, HttpStatus, ObjectWithUnknownFields } from "app/common/types/http.types";
import { FilterFieldBase } from "app/modules/filters/field/field-type";
import { FiltersPopUp } from "app/modules/filters/filters";
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";

export const getQAMetricsData = () => {
	return async (dispatch: any) => {
		dispatch(
			setQaMetricsStatuses({
				filter: HttpStatus.LOADING,
				data: HttpStatus.LOADING,
				table: HttpStatus.LOADING,
			})
		);

		let records_count: QAMetricsRecordsCount;

		if (await checkModelIsFound()) {
			dispatch(uploadQAMetricsFilters());
			records_count = await dispatch(getQAMetricsTotalStatistic());
		} else {
			dispatch(
				setQaMetricsStatuses({
					filter: HttpStatus.PREVIEW,
					data: HttpStatus.PREVIEW,
					table: HttpStatus.PREVIEW,
				})
			);
			return;
		}

		if (records_count.filtered) {
			dispatch(updateQAMetricsData());
		} else {
			dispatch(
				addToast(
					"With cached filters we didn't find data. Try to change filter.",
					ToastStyle.Warning
				)
			);

			dispatch(
				setQaMetricsStatuses({
					data: HttpStatus.PREVIEW,
					table: HttpStatus.PREVIEW,
				})
			);
		}
	};
};

export const getQAMetricsTotalStatistic = () => {
	return async (dispatch: any) => {
		let records_count: QAMetricsRecordsCount;

		try {
			records_count = await QaMetricsApi.getCount();
		} catch (e) {
			return;
		}

		dispatch(setQaMetricsRecordsCount(records_count));

		return records_count;
	};
};

export const uploadQAMetricsFilters = () => {
	return async (dispatch: any) => {
		dispatch(
			setQaMetricsStatuses({
				filter: HttpStatus.LOADING,
			})
		);

		let fields: FilterFieldBase[];

		try {
			fields = await QaMetricsApi.getFilters();
		} catch (e) {
			dispatch(
				setQaMetricsStatuses({
					filter: HttpStatus.FAILED,
				})
			);
			return;
		}

		dispatch(setQaMetricsFilter(fields));

		dispatch(
			setQaMetricsStatuses({
				filter: HttpStatus.FINISHED,
			})
		);
	};
};

export const applyQAMetricsFilters = (filters: FilterFieldBase[]) => {
	return async (dispatch: any) => {
		dispatch(
			setQaMetricsStatuses({
				filter: HttpStatus.LOADING,
				data: HttpStatus.LOADING,
				table: HttpStatus.RELOADING,
			})
		);

		let records_count: QAMetricsRecordsCount;

		try {
			records_count = await dispatch(saveQAMetricsFilters(filters));
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
			dispatch(
				setQaMetricsStatuses({
					filter: HttpStatus.FAILED,
				})
			);
			return;
		}

		if (records_count.filtered) {
			dispatch(updateQAMetricsData());
		} else {
			dispatch(
				setQaMetricsStatuses({
					data: HttpStatus.PREVIEW,
					table: HttpStatus.PREVIEW,
				})
			);

			dispatch(addToast(FiltersPopUp.noDataFound, ToastStyle.Warning));
		}
	};
};

export const saveQAMetricsFilters = (filters: FilterFieldBase[]) => {
	return async (dispatch: any) => {
		dispatch(
			setQaMetricsStatuses({
				filter: HttpStatus.LOADING,
			})
		);

		let response: {
			records_count: QAMetricsRecordsCount;
			filters: FilterFieldBase[];
		};

		try {
			response = await QaMetricsApi.saveFilters([...filters]);
		} catch (e) {
			dispatch(
				setQaMetricsStatuses({
					filter: HttpStatus.FAILED,
				})
			);
			return;
		}

		dispatch(setQaMetricsRecordsCount(response.records_count));
		dispatch(setQaMetricsFilter(response.filters));

		dispatch(
			setQaMetricsStatuses({
				filter: HttpStatus.FINISHED,
			})
		);

		return response.records_count;
	};
};

export const updateQAMetricsData = () => {
	return async (dispatch: any) => {
		dispatch(
			setQaMetricsStatuses({
				data: HttpStatus.LOADING,
				table: HttpStatus.LOADING,
			})
		);

		let test: QAMetricsAllData;

		try {
			test = await QaMetricsApi.getQAMetricsData();
		} catch (e) {
			dispatch(
				setQaMetricsStatuses({
					data: HttpStatus.FAILED,
					table: HttpStatus.FAILED,
				})
			);

			return;
		}

		dispatch(setQAMetricsAllData(test));

		dispatch(
			setQaMetricsStatuses({
				data: HttpStatus.FINISHED,
				table: HttpStatus.FINISHED,
			})
		);
	};
};

export const updateQAMetricsTable = (limit: number, offset: number) => {
	return async (dispatch: any) => {
		dispatch(
			setQaMetricsStatuses({
				table: HttpStatus.RELOADING,
			})
		);

		let response: ObjectWithUnknownFields[];

		try {
			response = await QaMetricsApi.getQAMetricsPredictionsTable(limit, offset);
		} catch (e) {
			dispatch(
				setQaMetricsStatuses({
					table: HttpStatus.FAILED,
				})
			);

			return;
		}

		dispatch(setQAMetricsTable(response));
		dispatch(
			setQaMetricsStatuses({
				table: HttpStatus.FINISHED,
			})
		);
	};
};
