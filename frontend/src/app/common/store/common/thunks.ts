import { AnalysisAndTrainingApi } from 'app/common/api/analysis-and-training.api';
import { markLoadIssuesFinished } from 'app/common/store/common/actions';
import { InitialApiResponse } from './types';

export const checkCollectingIssuesFinished = () => {
	return async (dispatch: any) => {
		try {
			const dataCollectingStatus: InitialApiResponse = await AnalysisAndTrainingApi.getGeneralApplicationStatus();
			if (dataCollectingStatus.issues_exists) dispatch(markLoadIssuesFinished());
		} catch (e) {
			return;
		}		
	}
}
