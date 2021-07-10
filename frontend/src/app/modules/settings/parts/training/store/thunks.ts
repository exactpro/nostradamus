/* eslint-disable consistent-return */
/* eslint-disable @typescript-eslint/no-unsafe-return */
/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */

// TODO: Declare static types for this thunk

import { SettingsApi } from "app/common/api/settings.api";
import { SettingsTrainingSendEntitiesAndResolution, SettingsTrainingSendSourceField, SettingsTrainingSendType, TrainingSubSection } from "app/modules/settings/parts/training/store/types";
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";
import { HttpStatus } from "app/common/types/http.types";
import {
    setSettingsTrainingData,
    setSettingsTrainingStatus,
    updateDefaultSourceField,
    updateDefaultEntitiesAndResolutionData,
} from "app/modules/settings/parts/training/store/actions";
import { markModelNotTrained } from "app/common/store/common/thunks";
import { uploadSignificantTermsData } from "app/common/store/analysis-and-training/thunks";

export const uploadSettingsTrainingSubfieldData = (subfield: TrainingSubSection) => {
    return async (dispatch: any) => {
        let res;
        try {
            res = await SettingsApi.getSettingsTrainingData(subfield);
        }
        catch (e) {
            dispatch(addToast(e.message, ToastStyle.Error));
            dispatch(setSettingsTrainingStatus({ [subfield]: HttpStatus.FAILED }));
            return;
        }
        dispatch(setSettingsTrainingData(res, subfield));
        dispatch(setSettingsTrainingStatus({ [subfield]: HttpStatus.FINISHED }));
        return res;
    }
}

export const sendSettingsTrainingData = (data: SettingsTrainingSendType, subfield?: TrainingSubSection.source_field) => {
    return async (dispatch: any) => {
        try {
            const res = await SettingsApi.sendSettingsTrainingDataData(data, subfield);

            if (subfield) {
                dispatch(updateDefaultSourceField(data as SettingsTrainingSendSourceField))
            } else {
                dispatch(updateDefaultEntitiesAndResolutionData(data as SettingsTrainingSendEntitiesAndResolution));
            }

            dispatch(markModelNotTrained());

            if (!subfield) {
                dispatch(uploadSignificantTermsData());
            }

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
            Object.values(TrainingSubSection).forEach(subfield => {
                dispatch(setSettingsTrainingStatus({ [subfield]: HttpStatus.RELOADING }));
                dispatch(uploadSettingsTrainingSubfieldData(subfield));
            })
        }
        catch (e) {
            dispatch(addToast(e.message, ToastStyle.Error));
        }
    }
}
