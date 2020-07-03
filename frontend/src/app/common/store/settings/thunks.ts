import {uploadData, setSettingsStatus} from "app/common/store/settings/actions";
import {SettingsSections, SettingsDataUnion} from "app/common/store/settings/types"
import {SettingsApi} from "app/common/api/settings.api"; 
import { getDashboardData } from "app/common/store/analysis-and-training/thunks";
import { HttpError, HttpStatus } from 'app/common/types/http.types';
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";

export const uploadSettings = (section: SettingsSections) => {
  return async (dispatch: any) => {
    dispatch(setSettingsStatus(section,HttpStatus.RELOADING))
    try{
      let res = await SettingsApi.getSettingsData(section)
      dispatch(uploadData(section, res))
      dispatch(setSettingsStatus(section, HttpStatus.FINISHED))
    }
    catch(e)
    {
			dispatch(setSettingsStatus(section, HttpStatus.FINISHED));
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
    }
  }
}

export const sendSettings =(section: SettingsSections, data: SettingsDataUnion) => {
  return async (dispatch: any) => {
    try{
      await SettingsApi.sendSettingsData(section, data);
      dispatch(uploadData(section, data))
      if(section === SettingsSections.filters) dispatch(getDashboardData());
    }
    catch(e){
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
    }
  }
}
