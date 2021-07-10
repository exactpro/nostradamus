import { FilterFieldBase } from 'app/modules/filters/field/field-type';
import { Terms } from 'app/modules/significant-terms/store/types';

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
	metrics: string[];
	chosen_metric: string | null;
	terms: Terms;
}

export interface DefectSubmissionData {
	created_line: LineData;
	resolved_line: LineData;
	created_total_count: number;
	resolved_total_count: number;
	period: string;
}
