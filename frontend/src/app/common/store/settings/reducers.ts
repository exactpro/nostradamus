import {SettingsStore, SettingsActionTypes} from "app/common/store/settings/types";
import { HttpStatus } from 'app/common/types/http.types';
import { InferValueTypes } from 'app/common/store/utils';
import {copyData} from "app/common/functions/helper";
import * as actions from './actions';

const initialState: SettingsStore = {
  isOpen: false,
  status: {
    filters:HttpStatus.FINISHED,
    qa_metrics:HttpStatus.FINISHED,
    predictions_table:HttpStatus.FINISHED,
    training:HttpStatus.FINISHED,
  },
  defaultSettings:{
    filters: [],
    qa_metrics: [],
    predictions_table: [],
    training: {
      mark_up_source: "",
      mark_up_entities: [],
      bug_resolution: [
        {
          metric: "Resolution",
          value: ""
        },
        {
          metric: "Resolution",
          value: ""
        }
      ]
    },
  },
}

type actionsUserTypes = ReturnType<InferValueTypes<typeof actions>>;

export const settingsReducer = (state: SettingsStore = initialState, action: actionsUserTypes) => {
  let defaultSettings = {...state.defaultSettings}, status = {...state.status}
  switch (action.type) {

    case SettingsActionTypes.activateSettings:
      return {...state, isOpen: !state.isOpen}

    case SettingsActionTypes.setSettingsStatus:
      status[action.section] = action.status
      return {...state, status}

    case SettingsActionTypes.uploadData:
      defaultSettings[action.section] = copyData(action.settings)
      return {...state, defaultSettings}

    default:
      return {...state}

  }
}
