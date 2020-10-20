
import { SettingsApi } from "app/common/api/settings.api";
import { TrainingSubSection } from "app/modules/settings/fields/settings_training/store/types";
import { SettingsSections } from "app/common/store/settings/types"
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";
import { setSettingsTrainingData, setSettingsTrainingStatus } from "./actions";
import { HttpStatus } from "app/common/types/http.types";

export const uploadSettingsTrainingSubfieldData = (subfield: TrainingSubSection) => {
    return async (dispatch: any) => {
        let res;
        try {
            res = await SettingsApi.getSettingsData(SettingsSections.training, subfield);
        }
        catch (e) {
            dispatch(addToast(e.message, ToastStyle.Error));
            dispatch(setSettingsTrainingStatus(HttpStatus.FAILED, subfield));
            return;
        }
        if (res.warning) {
            dispatch(setSettingsTrainingStatus(HttpStatus.FAILED, subfield));
            return
        }
        dispatch(setSettingsTrainingData(res, subfield));
        dispatch(setSettingsTrainingStatus(HttpStatus.FINISHED, subfield));
        return res;
    }
}

export const sendSettingsTrainingData = (data: any, subfield: TrainingSubSection) => {
    return async (dispatch: any) => {
        try {
            let res = await SettingsApi.sendSettingsData(SettingsSections.training, data, subfield);
            return res.result === "success";
        }
        catch (e) {
            dispatch(addToast(e.message, ToastStyle.Error));
        }
    }
}

export const uploadSettingsTrainingData = () => {
    return async (dispatch: any) => {
        try {
            Object.values(TrainingSubSection).forEach(item => {
                dispatch(setSettingsTrainingStatus(HttpStatus.RELOADING, item));
                dispatch(uploadSettingsTrainingSubfieldData(item));
            })
        }
        catch (e) {
            dispatch(addToast(e.message, ToastStyle.Error));
        }
    }
}