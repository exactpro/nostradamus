import {
	VirtualAssistantActionTypes,
	MessageSendingType,
	InboundData,
	OutboundData,
} from "app/common/store/virtual-assistant/types";

export const activateVirtualAssistant = () =>
	({
		type: VirtualAssistantActionTypes.activateVirtualAssistant,
	} as const);

export const activateMessage = (
	content: InboundData | OutboundData,
	messageType: MessageSendingType = MessageSendingType.outbound
) =>
	({
		type: VirtualAssistantActionTypes.activateMessage,
		message: {
			messageType,
			content,
		},
	} as const);

export const clearMessages = () =>
	({
		type: VirtualAssistantActionTypes.clearMessages,
	} as const);

export const setTypingStatus = (typingStatus = true) =>
	({
		typingStatus,
		type: VirtualAssistantActionTypes.setTypingStatus,
	} as const);
