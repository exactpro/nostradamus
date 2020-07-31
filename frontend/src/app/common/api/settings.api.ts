import { HttpClient } from 'app/common/api/http-client';
import {SettingsSections, SettingsDataUnion} from "app/common/store/settings/types";
import {copyData} from "app/common/functions/helper";

export class SettingsApi {

	static baseUrl: string = 'settings';

	public static async getSettingsData(section: SettingsSections, subSection?: string) {
		try {
			return await HttpClient.get(this.baseUrl + `/${section}/${subSection?subSection+'/':''}`);
		} catch (e) {
			throw e;
		}
	}


	public static async sendSettingsData(section: SettingsSections, data: SettingsDataUnion, subSection?: string) {
		try {
			return await HttpClient.post(this.baseUrl + `/${section}/${subSection?subSection+'/':''}`, {} , copyData(data) );
		} catch (e) {
			throw e;
		}
	}
}
