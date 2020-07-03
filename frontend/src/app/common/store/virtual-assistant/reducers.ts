import {VirtualAssistantStore, VirtualAssistantActionTypes} from "app/common/store/virtual-assistant/types";
import { InferValueTypes } from 'app/common/store/utils'; 
import * as actions from './actions';

const initialState: VirtualAssistantStore = {
  isOpen: false,
  messages: [],
}

type actionsUserTypes = ReturnType<InferValueTypes<typeof actions>>;

export const virtualAssistantReducer = (state: VirtualAssistantStore = initialState, action: actionsUserTypes) => {
  let messages = state.messages.slice()
  switch(action.type)
  {
    case VirtualAssistantActionTypes.activateVirtualAssistant:
      return {...state, isOpen:!state.isOpen}

    case VirtualAssistantActionTypes.activateMessage:
      messages.push({...action.message})
      return {...state, messages}

    default:
      return {...state}
  }
}
