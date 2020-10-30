/* eslint-disable import/prefer-default-export */
import HttpClient from "app/common/api/http-client";
import { copyData } from "app/common/functions/helper";
import { OutboundData } from "app/common/store/virtual-assistant/types";

export class VirtualAssistantApi {
	static baseUrl = "/virtual-assistant/webhooks/rest/webhook/";

	public static SendMessage(outboundData: OutboundData) {
		return HttpClient.post("", {}, copyData(outboundData), this.baseUrl);
	}
}
