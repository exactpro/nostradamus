import { DescriptionAssessmentApi } from "app/common/api/description-assessment.api";
import { fixTTRBarChartAxisDisplayStyle } from "app/common/functions/helper";
import { HttpError, HttpStatus } from "app/common/types/http.types";
import { PredictMetric } from "app/modules/predict-text/predict-text";
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";
import { setStatus, setKeywords, setMetrics, setProbabilities, setDAText } from "./actions";
import { Probabilities } from "./types";

export function getKeywords(predictMetric: PredictMetric) {
    return async (dispatch: any) => {

        // for reset keywords
        try {
            let newKeywords: string[];
            if (predictMetric.value) {
                newKeywords = await DescriptionAssessmentApi.getHighlightedTerms(predictMetric);
            } else {
                newKeywords = [];
            }
            dispatch(setKeywords(predictMetric.metric, newKeywords))

        } catch (e) {
            dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
        }
    }
}

export function getMetrics(empty: boolean = false) {
    return async (dispatch: any) => {
        try {
            const metrics = await DescriptionAssessmentApi.getMetrics();
            if (metrics.warning) {
                addToast(metrics.warning.detail, ToastStyle.Warning);
                return;
            }
            if (!empty) {
                dispatch(setMetrics(metrics));
            }

        } catch (e) {
            dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
        }
    }
}

export function predictText(text: string) {
    return async (dispatch: any) => {

        dispatch(setDAText(text));
        dispatch(setStatus(HttpStatus.LOADING));

        try {
            const data = await DescriptionAssessmentApi.predictText(text);

            if (data.warning) throw new Error(data.warning.detail || data.warning.message);

            dispatch(setStatus(HttpStatus.FINISHED))

            const probabilities: Probabilities = data;
            probabilities["Time to Resolve"] = fixTTRBarChartAxisDisplayStyle(probabilities["Time to Resolve"]);

            dispatch(setProbabilities(probabilities));
            dispatch(getMetrics())

        } catch (e) {
            dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
            dispatch(setStatus(HttpStatus.FAILED))
        }
    }
}
