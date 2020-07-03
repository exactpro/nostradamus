import { HttpStatus } from 'app/common/types/http.types';
import { FilterFieldBase } from 'app/modules/filters/field/field-type';

export interface AnalysisAndTrainingStore {
	status: HttpStatus,
	frequentlyTermsList: string[]
	statistic: AnalysisAndTrainingStatistic | null;
	defectSubmission: AnalysisAndTrainingDefectSubmission,
	isCollectingFinished: boolean
}

export type AnalysisAndTrainingDefectSubmission = { [key: string]: string } | null;

// TODO: refactor this to dynamic properties names
export interface AnalysisAndTrainingStatistic {
	[key: string]: StatisticPart,
	Comments: StatisticPart,
	Attachments: StatisticPart,
	"Time to Resolve": StatisticPart
}

export interface StatisticPart {
	minimum: string;
	maximum: string;
	mean: string;
	std: string;
}

export interface ApplyFilterBody {
	action: 'apply' | 'Clear',
	filters?: FilterFieldBase[]
}
