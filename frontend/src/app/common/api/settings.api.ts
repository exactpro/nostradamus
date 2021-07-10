/* eslint-disable import/prefer-default-export */
import HttpClient from "app/common/api/http-client";
import { FilterData, PredictionTableData } from "app/common/store/settings/types";
import { copyData } from "app/common/functions/helper";
import { SettingsTrainingSendType, TrainingSubSection } from "app/modules/settings/parts/training/store/types";

export class SettingsApi {
	static baseUrl = "settings";

	public static async getSettingsTrainingData(subSection?: string) {
		return HttpClient.get(`${this.baseUrl}/training/${subSection}/`);
	}

	public static async getSettingsATFiltersData() {
		return HttpClient.get(`${this.baseUrl}/filters/`);
	}

	public static async getSettingsQAMetricsFiltersData() {
		return HttpClient.get(`${this.baseUrl}/qa_metrics/`);
	}

	public static async getSettingsPredictionsData() {
		return HttpClient.get(`${this.baseUrl}/predictions_table/`);
	}

	public static async sendSettingsATFiltersData(
		data: FilterData[]) {
		return HttpClient.post(
			`${this.baseUrl}/filters/`,
			{},
			copyData(data)
		);
	}

	public static async sendSettingsQAMetricsFiltersData(
		data: FilterData[]) {
		return HttpClient.post(
			`${this.baseUrl}/qa_metrics/`,
			{},
			copyData(data)
		);
	}

	public static async sendSettingsPredictionsData(
		data: PredictionTableData[]) {
		return HttpClient.post(
			`${this.baseUrl}/predictions_table/`,
			{},
			copyData(data)
		);
	}

	public static async sendSettingsTrainingDataData(
		data: SettingsTrainingSendType,
		subSection?: TrainingSubSection) {
		return HttpClient.post(
			`${this.baseUrl}/training/${subSection ? `${subSection}/` : ""}`,
			{},
			copyData(data)
		);
	}
}
