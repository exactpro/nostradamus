import { AnalysisAndTrainingApi } from 'app/common/api/analysis-and-training.api';
import { HttpError, HttpStatus } from 'app/common/types/http.types';
import { addToast } from 'app/modules/toasts-overlay/store/actions';
import { ToastStyle } from 'app/modules/toasts-overlay/store/types';
import { trainingModelSetStatus } from 'app/modules/training-button/store/actions';

export const trainModel = () => {
	return async (dispatch: any) => {
		dispatch(trainingModelSetStatus(HttpStatus.LOADING));

		try {
			dispatch(addToast('Start training', ToastStyle.Info));
			await AnalysisAndTrainingApi.trainModel();
			dispatch(trainingModelSetStatus(HttpStatus.FINISHED));
		} catch (e) {
			dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Warning));
			dispatch(trainingModelSetStatus(HttpStatus.FAILED));
		}
	};
};
