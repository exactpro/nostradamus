import {VirtualAssistantActionTypes} from "app/common/store/virtual-assistant/types";
import {MessageSendingType, InboundData, OutboundData} from "app/common/store/virtual-assistant/types";

export const activateVirtualAssistant = () => ({
 type:VirtualAssistantActionTypes.activateVirtualAssistant
} as const)

export const activateMessage = (content: InboundData | OutboundData, messageType: MessageSendingType = MessageSendingType.outbound ) => ({
  type:VirtualAssistantActionTypes.activateMessage,
  message:{
    messageType,
    content,
  }
} as const)
