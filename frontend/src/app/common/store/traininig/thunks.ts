import { AnalysisAndTrainingApi } from "app/common/api/analysis-and-training.api";
import { markModelNotTrained, searchTrainedModel } from "app/common/store/common/thunks";
import { setTrainingStatus } from "app/common/store/traininig/actions";
import { HttpError, HttpStatus } from "app/common/types/http.types";
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";

export const startTrainModel = () => {
	return async (dispatch: any) => {
		dispatch(markModelNotTrained());
		dispatch(setTrainingStatus(HttpStatus.RELOADING));
		dispatch(addToast("Start training", ToastStyle.Info));

		try {
			await AnalysisAndTrainingApi.trainModel();
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error));
			dispatch(setTrainingStatus(HttpStatus.FAILED));
			return;
		}

		dispatch(searchTrainedModel());
		dispatch(setTrainingStatus(HttpStatus.FINISHED));
	};
};
