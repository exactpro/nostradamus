import { AnalysisAndTrainingStore } from 'app/common/store/analysis-and-training/types';
import { InferValueTypes } from 'app/common/store/utils';
import { HttpStatus } from 'app/common/types/http.types';
import mainStatistic from 'app/modules/main-statistic/store';
import significantTerms from 'app/modules/significant-terms/store/reducer';
import trainingModel from 'app/modules/training-button/store/reducer';
import { combineReducers } from 'redux';
import * as actions from './actions';

const initialState: AnalysisAndTrainingStore = {
	status: HttpStatus.PREVIEW,
	frequentlyTermsList: [],
	statistic: null,
	defectSubmission: null,
	isCollectingFinished: true,
};

type actionsAnalysisAndTrainingTypes = ReturnType<InferValueTypes<typeof actions>>;

function analysisAndTraining(state: AnalysisAndTrainingStore = initialState, action: actionsAnalysisAndTrainingTypes): AnalysisAndTrainingStore {
	switch (action.type) {

		case 'SET_STATUS':
			return {
				...state,
				status: action.newStatus,
			};

		case 'SET_FREQUENTLY_TERMS':
			return {
				...state,
				frequentlyTermsList: action.frequentlyTermsList,
			};

		case 'SET_ANALYSIS_AND_TRAINING_FREQUENTLY_TERMS':
			return {
				...state,
				statistic: { ...action.statistic },
			};

		case 'SET_ANALYSIS_AND_TRAINING_DEFECT_SUBMISSION':
			return {
				...state,
				defectSubmission: { ...action.defectSubmission },
			};

		case 'ANALYSIS_AND_TRAINING_SET_COLLECTING_FINISH': {
			return {
				...state,
				isCollectingFinished: action.newStatus,
			};
		}

		default:
			return state;
	}
}

export const analysisAndTrainingStore = combineReducers({
	analysisAndTraining,
	mainStatistic,
	significantTerms,
	trainingModel,
});
