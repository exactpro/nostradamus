import { ChartData } from "app/common/components/charts/types";
import { InferValueTypes } from "app/common/store/utils";
import { HttpStatus } from "app/common/types/http.types";
import * as actions from "./actions";
import {
	DAPrioritySortBy,
	DescriptionAssessmentActionTypes,
	DescriptionAssessmentStore,
} from "./types";

const initialState: DescriptionAssessmentStore = {
	status: HttpStatus.PREVIEW,
	text: '',
	metrics: {
		Priority: [],
		resolution: [],
		areas_of_testing: [],
	},
	keywords: {
		Priority: [],
		resolution: [],
		areas_of_testing: [],
	},
	probabilities: null,
};


type actionsUserTypes = ReturnType<InferValueTypes<typeof actions>>;

export default function descriptionAssessmentReducer(state: DescriptionAssessmentStore = initialState, action: actionsUserTypes) {
    switch (action.type) {
			case DescriptionAssessmentActionTypes.setStatus:
				return { ...state, status: action.status };

			case DescriptionAssessmentActionTypes.setKeywords:
				const keywords = { ...state.keywords };
				keywords[action.metricName] = [...action.keyWords];
				return { ...state, keywords };

			case DescriptionAssessmentActionTypes.setMetrics:
				return { ...state, metrics: action.metrics };

			case DescriptionAssessmentActionTypes.setProbabilities:
				return {
					...state,
					probabilities: {
						...action.probabilities,
						Priority: [...sortPriority(action.probabilities.Priority, DAPrioritySortBy.Value)],
					},
				};

	    case DescriptionAssessmentActionTypes.setText:
	    	return {
	    		...state,
			    text: action.text
		    }

			case DescriptionAssessmentActionTypes.sortPriority:
				return {
					...state,
					probabilities: {
						...state.probabilities!,
						Priority: [ ...sortPriority(state.probabilities!.Priority, action.sortBy)]
					},
				};

			case DescriptionAssessmentActionTypes.clearPredictionText:
				return { ...initialState };

			default:
				return { ...state };
		}
}

function sortPriority(
  chartData: ChartData,
  fieldName: DAPrioritySortBy
): ChartData {
    return chartData.sort((a, b) => {
        if (fieldName === DAPrioritySortBy.Value) {
            return a[fieldName] < b[fieldName] ? 1 : -1;
        }
        return a[fieldName] < b[fieldName] ? -1 : 1;
    })
}
