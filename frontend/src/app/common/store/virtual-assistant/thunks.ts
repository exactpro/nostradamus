/* eslint-disable @typescript-eslint/no-unsafe-member-access */
/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable import/prefer-default-export */

// TODO: Declare static types for this thunk

import { VirtualAssistantApi } from "app/common/api/virtual-assistant.api";
import { activateMessage, setTypingStatus } from "app/common/store/virtual-assistant/actions";
import { MessageSendingType, InboundData } from "app/common/store/virtual-assistant/types";
import { HttpError } from "app/common/types/http.types";
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";
import { RootStore } from "app/common/types/store.types";
import QueueGenerator from "app/common/store/virtual-assistant/queue-generator";

let queueGenerator: QueueGenerator<InboundData>;

export const sendVirtualAssistantMessage = (outboundMessage: string, outboundRenderMessage?: string) => {
  return async (dispatch: any, getState: () => RootStore) => {

    if (!queueGenerator) queueGenerator = new QueueGenerator(queueAction(dispatch), 3000, () => dispatch(setTypingStatus()));

    try {
      const userId = getState().auth.user?.id || "sender";

      dispatch(activateMessage({ sender: userId, message: outboundRenderMessage || outboundMessage }));

      dispatch(setTypingStatus());
      const response: InboundData[] = await VirtualAssistantApi.SendMessage({ sender: userId, message: outboundMessage });
      queueGenerator.pushQueueArguments(response);

    }
    catch (e) {
      dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
    }
  }
};

const queueAction = (dispatch: any) => {
  return (message: InboundData) => {
    dispatch(activateMessage(message, MessageSendingType.inbound));
    dispatch(setTypingStatus(false));
  }
}