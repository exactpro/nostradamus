import {
	AnalysisAndTrainingDefectSubmission,
	AnalysisAndTrainingStatistic,
} from 'app/common/store/analysis-and-training/types';
import { HttpStatus } from 'app/common/types/http.types';

export const changeStatus = (newStatus: HttpStatus) => ({
	type: 'SET_STATUS',
	newStatus: newStatus,
} as const);

export const setIsCollectingFinish = (status: boolean) => ({
	type: 'ANALYSIS_AND_TRAINING_SET_COLLECTING_FINISH',
	newStatus: status,
} as const);

export const updateFrequentlyTerms = (frequentlyTermsList: string[]) => ({
	type: 'SET_FREQUENTLY_TERMS',
	frequentlyTermsList,
} as const);

export const setAnalysisAndTrainingStatistic = (statistic: AnalysisAndTrainingStatistic) => ({
	type: 'SET_ANALYSIS_AND_TRAINING_FREQUENTLY_TERMS',
	statistic,
} as const);

export const setDefectSubmission = (defectSubmission: AnalysisAndTrainingDefectSubmission) => ({
	type: 'SET_ANALYSIS_AND_TRAINING_DEFECT_SUBMISSION',
	defectSubmission,
} as const);
