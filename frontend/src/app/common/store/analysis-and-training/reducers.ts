import { AnalysisAndTrainingStore } from "app/common/store/analysis-and-training/types";
import { InferValueTypes } from "app/common/store/utils";
import { HttpStatus } from "app/common/types/http.types";
import * as actions from "./actions";

const initialState: AnalysisAndTrainingStore = {
	filters: [],
	totalStatistic: undefined,
	frequentlyTerms: [],
	statistic: {},
	significantTerms: {
		metrics: [],
		chosen_metric: null,
		terms: {},
	},
	defectSubmission: {
		created_line: {},
		resolved_line: {},
		created_total_count: 0,
		resolved_total_count: 0,
		period: "",
	},
	statuses: {
		filter: HttpStatus.PREVIEW,
		frequentlyTerms: HttpStatus.PREVIEW,
		defectSubmission: HttpStatus.PREVIEW,
		statistic: HttpStatus.PREVIEW,
		significantTerms: HttpStatus.PREVIEW,
	},
	warnings: {
		frequentlyTerms: '',
		significantTerms: '',
	},
};

type actionsUserTypes = ReturnType<InferValueTypes<typeof actions>>;

export const analysisAndTrainingReducers = (state: AnalysisAndTrainingStore = initialState, action: actionsUserTypes): AnalysisAndTrainingStore => {
	switch (action.type) {

		case "SET_A&T_STATUSES": return {
			...state,
			statuses: {
				...state.statuses,
				...action.statuses
			}
		}

		case "SET_A&T_WARNINGS": return {
			...state,
			warnings: {
				...state.warnings,
				...action.warnings
			}
		}

		case "SET_A&T_SIGNIFICANT_TERMS": return {
			...state,
			significantTerms: {
				...action.significantTerms
			}
		}

		case "UPDATE_A&T_SIGNIFICANT_TERMS_CHOSEN_METRIC": return {
			...state,
			significantTerms: {
				...state.significantTerms,
				chosen_metric: action.metric
			}
		}

		case "UPDATE_A&T_SIGNIFICANT_TERMS_LIST": return  {
			...state,
			significantTerms: {
				...state.significantTerms,
				terms: { ...action.terms }
			}
		}

		case "SET_A&T_DEFECT_SUBMISSION": return {
			...state,
			defectSubmission: {
				...action.defectSubmission
			}
		}

		case "SET_A&T_FREQUENTLY_TERMS": return {
			...state,
			frequentlyTerms: [ ...action.frequentlyTerms ]
		}

		case "SET_A&T_STATISTIC": return {
			...state,
			statistic: {
				...action.statistic
			}
		}

		case "SET_A&T_FILTERS": return {
			...state,
			filters: [ ...action.filters ]
		}

		case "SET_A&T_TOTAL_STATISTIC": return {
			...state,
			totalStatistic: {
				...action.statistic
			}
		}

		default:
			return { ...state };
	}
};
