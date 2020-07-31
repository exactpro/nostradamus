import {SettingsActionTypes, SettingsSections, SettingsDataUnion} from "app/common/store/settings/types";
import { HttpStatus } from 'app/common/types/http.types';

export const activateSettings = () => ({
  type: SettingsActionTypes.activateSettings
} as const)

export const setSettingsStatus = (section: SettingsSections, status: HttpStatus) => ({
  status,
  section,
  type: SettingsActionTypes.setSettingsStatus
} as const);

export const uploadData = (section: SettingsSections, settings: SettingsDataUnion) => ({
  section,
  settings,
  type: SettingsActionTypes.uploadData
} as const);

export const setCollectingDataStatus = (isCollectionFinished: boolean) => ({
  isCollectionFinished,
  type: SettingsActionTypes.setCollectingDataStatus
} as const);

export const clearSettings = () => ({
  type: SettingsActionTypes.clearSettings
} as const);