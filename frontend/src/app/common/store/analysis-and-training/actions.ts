import {
	AnalysisAndTrainingStatuses,
	AnalysisAndTrainingWarnings
} from "app/common/store/analysis-and-training/types";
import {
	AnalysisAndTrainingStatistic,
	DefectSubmissionData,
	SignificantTermsData,
} from "app/common/types/analysis-and-training.types";
import { FilterFieldBase } from "app/modules/filters/field/field-type";
import { MainStatisticData } from "app/modules/main-statistic/main-statistic";
import { Terms } from "app/modules/significant-terms/store/types";

export const setTotalStatistic = (statistic: MainStatisticData) =>
	({
		type: "SET_A&T_TOTAL_STATISTIC",
		statistic,
	} as const);

export const setSignificantTerms = (significantTerms: SignificantTermsData) =>
	({
		type: "SET_A&T_SIGNIFICANT_TERMS",
		significantTerms,
	} as const);

export const updateSignificantTermsChosenMetric = (metric: string) =>
	({
		type: "UPDATE_A&T_SIGNIFICANT_TERMS_CHOSEN_METRIC",
		metric,
	} as const);

export const updateSignificantTermsList = (terms: Terms) =>
	({
		type: "UPDATE_A&T_SIGNIFICANT_TERMS_LIST",
		terms,
	} as const);

export const setDefectSubmission = (defectSubmission: DefectSubmissionData) =>
	({
		type: "SET_A&T_DEFECT_SUBMISSION",
		defectSubmission,
	} as const);

export const setFrequentlyTerms = (frequentlyTerms: string[]) =>
	({
		type: "SET_A&T_FREQUENTLY_TERMS",
		frequentlyTerms,
	} as const);

export const setStatistic = (statistic: AnalysisAndTrainingStatistic) =>
	({
		type: "SET_A&T_STATISTIC",
		statistic,
	} as const);

export const setCardStatuses = (statuses: Partial<AnalysisAndTrainingStatuses>) =>
	({
		type: "SET_A&T_STATUSES",
		statuses,
	} as const);

export const setCardWarnings = (warnings: Partial<AnalysisAndTrainingWarnings>) =>
	({
		type: "SET_A&T_WARNINGS",
		warnings,
	} as const);


export const setFilters = (filters: FilterFieldBase[]) =>
	({
		type: "SET_A&T_FILTERS",
		filters,
	} as const);
