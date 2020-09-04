import {uploadData, setSettingsStatus} from "app/common/store/settings/actions";
import {SettingsSections, SettingsDataUnion} from "app/common/store/settings/types"
import {SettingsApi} from "app/common/api/settings.api";
import { HttpError, HttpStatus } from 'app/common/types/http.types';
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";
import { clearSettingsTrainingData } from "app/modules/settings/fields/settings_training/store/actions";
import { clearSettings } from "app/common/store/settings/actions";

export const uploadSettingsData = (section: SettingsSections) => {
  return async (dispatch: any) => {
    dispatch(setSettingsStatus(section,HttpStatus.RELOADING))
    try{
      let res = await SettingsApi.getSettingsData(section);
      
      if(res.warning) { 
        dispatch(addToast(res.warning.detail, ToastStyle.Warning));
        dispatch(setSettingsStatus(section, HttpStatus.FAILED));
      }
      else{
        dispatch(uploadData(section, res));
        dispatch(setSettingsStatus(section, HttpStatus.FINISHED));
      }
    }
    catch(e)
    {
			dispatch(setSettingsStatus(section, HttpStatus.FAILED));
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
    }
  }
}

export const sendSettingsData =(section: SettingsSections, data: SettingsDataUnion | any) => {
  return async (dispatch: any) => {
    try{
      await SettingsApi.sendSettingsData(section, data);
    }
    catch(e){
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
    }
  }
}

export const clearSettingsData = () => {
  return (dispatch: any) => {
    dispatch(clearSettings());
    dispatch(clearSettingsTrainingData());
  }
} 


