import { AnalysisAndTrainingApi } from 'app/common/api/analysis-and-training.api';
import { markLoadBugsFinished } from 'app/common/store/common/actions';

export const checkCollectingDataFinished = () => {
	return async (dispatch: any) => {

		let totalStatistic;

		try {
			totalStatistic = await AnalysisAndTrainingApi.getTotalStatistic();
		} catch (e) {
			return;
		}

		if (totalStatistic.records_count) {
			dispatch(markLoadBugsFinished());
		}
	}
}
