import {VirtualAssistantApi} from "app/common/api/virtual-assistant.api";
import {activateMessage} from "app/common/store/virtual-assistant/actions";
import {MessageSendingType, InboundData} from "app/common/store/virtual-assistant/types";
import { HttpError } from 'app/common/types/http.types';
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";

export const sendVirtualAssistantMessage = (outboundMessage: string, outboundRenderMessage?: string) => {
  return async (dispatch:any) =>{
    try{
      dispatch(activateMessage({sender: "user", message: outboundRenderMessage? outboundRenderMessage: outboundMessage}));
      let response: InboundData[] = await VirtualAssistantApi.SendMessage({sender: "user", message: outboundMessage});
      
      if(response.length)
      (response as InboundData[]).forEach((element: InboundData) => {
        dispatch(activateMessage(element, MessageSendingType.inbound));
      });

    }
    catch(e){
      dispatch(addToast((e as HttpError).detail || e.message, ToastStyle.Error))
    }
  }
};
