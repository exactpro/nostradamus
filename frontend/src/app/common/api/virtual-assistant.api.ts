import { HttpClient } from 'app/common/api/http-client';
import {copyData} from "app/common/functions/helper";
import {OutboundData} from "app/common/store/virtual-assistant/types";

export class VirtualAssistantApi{

	static baseUrl: string = '/virtual-assistant/webhooks/rest/webhook/';

  public static async SendMessage(outboundData: OutboundData){
    try{
      return await HttpClient.post("", {}, copyData(outboundData), this.baseUrl)
    }
    catch(e){
      throw e;
    }
  }
}
