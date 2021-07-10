import { HttpStatus } from "app/common/types/http.types";
import { PredictMetricsName } from "app/modules/predict-text/predict-text";
import {
    DAPrioritySortBy,
    DescriptionAssessmentActionTypes,
    Keywords,
    Probabilities
} from "./types";

export const setStatus = (status: HttpStatus) => ({
    status,
    type: DescriptionAssessmentActionTypes.setStatus
} as const)

export const clearPageData = () => ({
    type: DescriptionAssessmentActionTypes.clearPredictionText
} as const)

export const setDAText = (text: string) => ({
    text,
    type: DescriptionAssessmentActionTypes.setText
} as const)

export const setKeywords = (metricName: PredictMetricsName, keyWords: string[]) => ({
    keyWords,
    metricName,
    type: DescriptionAssessmentActionTypes.setKeywords
} as const)

export const setMetrics = (metrics: Keywords) => ({
    metrics,
    type: DescriptionAssessmentActionTypes.setMetrics
} as const)

export const setProbabilities = (probabilities: Probabilities) => ({
    probabilities,
    type: DescriptionAssessmentActionTypes.setProbabilities
} as const)

export const sortDAPriority = (sortBy: DAPrioritySortBy) => ({
      sortBy,
      type: DescriptionAssessmentActionTypes.sortPriority,
  } as const);
