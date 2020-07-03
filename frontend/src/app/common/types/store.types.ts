import { QAMetricsStore } from 'app/common/store/qa-metrics/types';
import {MainStatistic} from "app/modules/main-statistic/types";
import {AnalysisAndTrainingStore} from "app/common/store/analysis-and-training/types";
import {AuthStore} from "app/common/store/auth/types";
import {SettingsStore} from "app/common/store/settings/types";
import {VirtualAssistantStore} from "app/common/store/virtual-assistant/types";
import { SignificantTermsState } from 'app/modules/significant-terms/store/types';
import { ToastStore } from 'app/modules/toasts-overlay/store/types';
import { TrainingModelState } from 'app/modules/training-button/store/types';

export interface RootStore {
  analysisAndTraining: {
    analysisAndTraining: AnalysisAndTrainingStore
    mainStatistic: MainStatistic
    significantTerms: SignificantTermsState,
    trainingModel: TrainingModelState
  },
  toasts: ToastStore,
  auth: AuthStore,
  settings: SettingsStore,
  virtualAssistant: VirtualAssistantStore,
  qaMetricsPage: QAMetricsStore
}
