import { ChartData, ChartsList } from "app/common/components/charts/types";
import { HttpStatus } from "app/common/types/http.types";
import { Terms } from "app/modules/significant-terms/store/types";

export interface Probabilities {
	resolution: ChartsList;
	areas_of_testing: Terms;
	"Time to Resolve": ChartData;
	Priority: ChartData;
}

export interface Keywords {
	Priority: string[];
	resolution: string[];
	areas_of_testing: string[];
}

export enum DAPrioritySortBy {
	Value = 'value',
	Name = 'name'
}

export interface DescriptionAssessmentStore {
	text: string;
	status: HttpStatus;
	metrics: Keywords;
	keywords: Keywords;
	probabilities: Probabilities | null;
}

export enum DescriptionAssessmentActionTypes {
	setStatus = "SET_STATUS",
	clearPredictionText = "CLEAR_PREDICTION_TEXT",
	setKeywords = "SET_KEYWORDS",
	setText = "SET_TEXT",
	setMetrics = "SET_METRICS",
	setProbabilities = "SET_PROBABILITIES",
	sortPriority = "DA_SORT_PRIORITY"
}
