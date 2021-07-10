import {
  AnalysisAndTrainingStatistic, DefectSubmissionData,
  SignificantTermsData
} from "app/common/types/analysis-and-training.types";
import { HttpStatus } from "app/common/types/http.types";
import { FilterFieldBase } from "app/modules/filters/field/field-type";
import { MainStatisticData } from "app/modules/main-statistic/main-statistic";

export interface AnalysisAndTrainingStatuses  {
  filter: HttpStatus;
  frequentlyTerms: HttpStatus;
  defectSubmission: HttpStatus;
  statistic: HttpStatus;
  significantTerms: HttpStatus;
};

export interface AnalysisAndTrainingWarnings  {
  frequentlyTerms: string;
  significantTerms: string;
};

export interface AnalysisAndTrainingStore {
  filters: FilterFieldBase[];
  totalStatistic: MainStatisticData | undefined;
  frequentlyTerms: string[];
  statistic: AnalysisAndTrainingStatistic;
  significantTerms: SignificantTermsData;
  defectSubmission: DefectSubmissionData;
  statuses: AnalysisAndTrainingStatuses;
  warnings: AnalysisAndTrainingWarnings;
}
