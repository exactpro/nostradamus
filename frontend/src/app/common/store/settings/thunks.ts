import { uploadData, setSettingsStatus, clearSettings, setATFiltersDefaultData, setQAMetricsFiltersDefaultData, setPredictionsDefaultData } from "app/common/store/settings/actions";
import { SettingsSections, PredictionTableData, FilterData } from "app/common/store/settings/types"
import { SettingsApi } from "app/common/api/settings.api";
import { HttpError, HttpStatus } from 'app/common/types/http.types';
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";
import { clearSettingsTrainingData } from "app/modules/settings/parts/training/store/actions";

export const uploadSettingsATFilterData = () => {
  return async (dispatch: any) => {
    dispatch(setSettingsStatus({ [SettingsSections.filters]: HttpStatus.RELOADING }))
    let res;

    try {
      res = await SettingsApi.getSettingsATFiltersData();
    }
    catch (e) {
      dispatch(riseSettingsError(SettingsSections.filters, (e as HttpError).detail || e.message));
      return;
    }
    dispatch(uploadData(SettingsSections.filters, res));
    dispatch(setSettingsStatus({ [SettingsSections.filters]: HttpStatus.FINISHED }));
  }
}

export const uploadSettingsQAMetricsFilterData = () => {
  return async (dispatch: any) => {
    dispatch(setSettingsStatus({ [SettingsSections.qaFilters]: HttpStatus.RELOADING }))
    let res;

    try {
      res = await SettingsApi.getSettingsQAMetricsFiltersData();
    }
    catch (e) {
      dispatch(riseSettingsError(SettingsSections.qaFilters, (e as HttpError).detail || e.message));
      return;
    }
    dispatch(uploadData(SettingsSections.qaFilters, res));
    dispatch(setSettingsStatus({ [SettingsSections.qaFilters]: HttpStatus.FINISHED }));
  }
}

export const uploadSettingsPredictionsData = () => {
  return async (dispatch: any) => {
    dispatch(setSettingsStatus({ [SettingsSections.predictions]: HttpStatus.RELOADING }))
    let res;

    try {
      res = await SettingsApi.getSettingsPredictionsData();
    }
    catch (e) {
      dispatch(riseSettingsError(SettingsSections.predictions, (e as HttpError).detail || e.message));
      return;
    }
    dispatch(uploadData(SettingsSections.predictions, res));
    dispatch(setSettingsStatus({ [SettingsSections.predictions]: HttpStatus.FINISHED }));
  }
}

export const sendSettingsATFiltersData = (data: FilterData[]) => {
  return async (dispatch: any) => {
    try {
      await SettingsApi.sendSettingsATFiltersData(data);
      dispatch(setATFiltersDefaultData(data));
    }
    catch (e) {
      dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
    }
  }
}

export const sendSettingsQAMetricsFiltersData = (data: FilterData[]) => {
  return async (dispatch: any) => {
    try {
      await SettingsApi.sendSettingsQAMetricsFiltersData(data);
      dispatch(setQAMetricsFiltersDefaultData(data));
    }
    catch (e) {
      dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
    }
  }
}

export const sendSettingsPredictionsData = (data: PredictionTableData[]) => {
  return async (dispatch: any) => {
    try {
      await SettingsApi.sendSettingsPredictionsData(data);
      dispatch(setPredictionsDefaultData(data))

    }
    catch (e) {
      dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
    }
  }
}

const riseSettingsError = (section: SettingsSections, errorTitle: string, toastStyle: ToastStyle = ToastStyle.Error) => {
  return (dispatch: any) => {
    dispatch(addToast(errorTitle, toastStyle));
    dispatch(setSettingsStatus({ [section]: HttpStatus.FAILED }));
  }
}

export const clearSettingsData = () => {
  return (dispatch: any) => {
    dispatch(clearSettings());
    dispatch(clearSettingsTrainingData());
  }
}