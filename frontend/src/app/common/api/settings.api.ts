/* eslint-disable import/prefer-default-export */
import HttpClient from "app/common/api/http-client";
import { SettingsSections, SettingsDataUnion } from "app/common/store/settings/types";
import { copyData } from "app/common/functions/helper";

export class SettingsApi {
	static baseUrl = "settings";

	public static async getSettingsData(section: SettingsSections, subSection?: string) {
		return HttpClient.get(`${this.baseUrl}/${section}/${subSection ? `${subSection}/` : ""}`);
	}

	public static async sendSettingsData(
		section: SettingsSections,
		data: SettingsDataUnion,
		subSection?: string
	) {
		return HttpClient.post(
			`${this.baseUrl}/${section}/${subSection ? `${subSection}/` : ""}`,
			{},
			copyData(data)
		);
	}
}
