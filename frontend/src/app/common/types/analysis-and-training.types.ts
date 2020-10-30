import { HttpStatus } from 'app/common/types/http.types';
import { FilterFieldBase } from 'app/modules/filters/field/field-type';
import { Terms } from 'app/modules/significant-terms/store/types';

export interface AnalysisAndTrainingStore {
	status: HttpStatus;
	frequentlyTermsList: string[];
	statistic: AnalysisAndTrainingStatistic | null;
	defectSubmission: AnalysisAndTrainingDefectSubmission;
	isCollectingFinished: boolean;
}

export type AnalysisAndTrainingDefectSubmission = {
	created_line: LineData;
	resolved_line: LineData;
	created_total_count: number;
	resolved_total_count: number;
	period: string;
} | null;

type LineData = {
	[key: string]: number;
};

// TODO: refactor this to dynamic properties names
export interface AnalysisAndTrainingStatistic {
	[key: string]: StatisticPart;
}

export interface StatisticPart {
	[key: string]: string;
}

export interface ApplyFilterBody {
	action: "apply" | "Clear";
	filters?: FilterFieldBase[];
}

export interface SignificantTermsData {
	metrics: string[],
	chosen_metric: string | null,
	terms: Terms
}

export interface DefectSubmissionData {
	data: AnalysisAndTrainingDefectSubmission | undefined,
	activePeriod: string | undefined,
}
