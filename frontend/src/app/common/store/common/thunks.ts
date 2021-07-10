import { AnalysisAndTrainingApi } from "app/common/api/analysis-and-training.api";
import { updateCommonStatuses } from "app/common/store/common/actions";
import { clearQAMetricsData } from "app/common/store/qa-metrics/actions";
import { setTrainingStatus } from "app/common/store/traininig/actions";
import { HttpStatus } from "app/common/types/http.types";
import { clearPageData as clearDAPageData } from "app/common/store/description-assessment/actions";
import { InitialApiResponse } from "./types";

export const checkIssuesStatus = () => {
	return async (dispatch: any) => {
		dispatch(
			updateCommonStatuses({
				isLoadedIssuesStatus: false,
			})
		);

		let issuesStatus: InitialApiResponse;

		try {
			issuesStatus = await AnalysisAndTrainingApi.getCollectingDataStatus();
		} catch (e) {
			return;
		}

		dispatch(
			updateCommonStatuses({
				isLoadedIssuesStatus: true,
				isIssuesExist: issuesStatus.issues_exists,
			})
		);

	};
};

export const searchTrainedModel = () => {
	return async (dispatch: any) => {
		dispatch(
			updateCommonStatuses({
				isSearchingModelFinished: false,
			})
		);

		let isTrainedModel: boolean;

		try {
			isTrainedModel = await AnalysisAndTrainingApi.getTrainingModelStatus();
		} catch (e) {
			return;
		}


		dispatch(setTrainingStatus(isTrainedModel ? HttpStatus.FINISHED : HttpStatus.PREVIEW));

		dispatch(
			updateCommonStatuses({
				isSearchingModelFinished: true,
				isModelFounded: isTrainedModel,
			})
		);
	};
};

export const markModelNotTrained = () => {
	return async (dispatch: any) => {
		dispatch(
			updateCommonStatuses({
				isSearchingModelFinished: true,
				isModelFounded: false,
			})
		);
		dispatch(setTrainingStatus(HttpStatus.PREVIEW))
		dispatch(clearDAPageData());
		dispatch(clearQAMetricsData());
	};
};
