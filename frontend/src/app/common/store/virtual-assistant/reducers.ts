import {
	VirtualAssistantStore,
	VirtualAssistantActionTypes,
} from "app/common/store/virtual-assistant/types";
import { InferValueTypes } from "app/common/store/utils";
import * as actions from "app/common/store/virtual-assistant/actions";

const initialState: VirtualAssistantStore = {
	isOpen: false,
	messages: [],
	typingStatus: false
};

type actionsUserTypes = ReturnType<InferValueTypes<typeof actions>>;

export default function virtualAssistantReducer(
	state: VirtualAssistantStore = initialState,
	action: actionsUserTypes
): VirtualAssistantStore {
	switch (action.type) {
		case VirtualAssistantActionTypes.activateVirtualAssistant:
			return { ...state, isOpen: !state.isOpen };

		case VirtualAssistantActionTypes.activateMessage:
			const messages = [{ ...action.message }, ...state.messages];
			return { ...state, messages };

		case VirtualAssistantActionTypes.setTypingStatus:
			return { ...state, typingStatus: action.typingStatus };

		case VirtualAssistantActionTypes.clearMessages:
			return { ...initialState };

		default:
			return { ...state };
	}
}
