import { HttpStatus } from 'app/common/types/http.types';

 export enum SettingsActionTypes{
  activateSettings = "ACTIVATE_SETTINGS",
  setSettingsStatus = "SET_SETTINGS_STATUS",
  uploadData = "UPLOAD_DATA",
  setData = "SET_DATA",
  clearData = "CLEAR_DATA",
  sendData = "SEND_DATA",
}

export enum SettingsSections{
  filters = "filters",
  qaFilters = "qa_metrics",
  predictions = "predictions_table",
  training = "training",
}

// Type for Filter section: Analysis&Training and QAMetrics
export type FilterType = {
  name: string,
  filtration_type: string,
}
// Type for PredictionTable section
export type PredictionTableType = {
  name: string,
  is_default: false,
  position: number,
}

// Type for Training section

export type MarkUpEntities = {
  area_of_testing: string,
  entities: string[],
}

export type BugResolution = {
  metric: string,
  value: string
}

export type TrainingType = {
  mark_up_source: string,
  mark_up_entities: MarkUpEntities[],
  bug_resolution: BugResolution[],
}

export type SettingsDataUnion = FilterType[] | PredictionTableType[] | TrainingType;

export interface SettignsData{
  filters: FilterType[],
  qa_metrics: FilterType[],
  predictions_table: PredictionTableType[],
  training: TrainingType,
}

export interface SettingsStore{
  isOpen: boolean,
  status: {[key: string]: HttpStatus},
  defaultSettings: SettignsData,
}
