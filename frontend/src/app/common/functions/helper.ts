import { ChartData } from "app/common/components/charts/types";
import { ObjectWithUnknownFields } from "app/common/types/http.types";

export function isOneOf<T>(requiredElem: T, allElem: T[]): boolean {
	return allElem.findIndex((elem) => elem === requiredElem) > -1;
}

export function deleteExtraSpaces(str: string): string {
	return str.replace(/\s+/g, " ").trim();
}

export function copyData(data: any) {
	if (Array.isArray(data)) return [...data];
	if (typeof data === "object") return { ...data };
	return data;
}

export function deepCopyData<T>(data: T) {
	return JSON.parse(JSON.stringify(data)) as T;
}

export const isStrIncludesSubstr = (str: string, substr: string) => {
	return str.toUpperCase().includes(substr.toUpperCase());
};

export function caseInsensitiveStringCompare(a: string, b: string) {
	return a.trim().localeCompare(b.trim(), undefined, { numeric: true, sensitivity: "base" });
}

// TTR processing functions

function sortByTTRKeys(ttrData: ChartData) {
	return ttrData.sort((a, b) => {
		const splitRegex = /(-| |>)+/;
		const aArr = a.name.split(splitRegex);
		const bArr = b.name.split(splitRegex);

		if (!aArr[0].length || (Number(aArr[0]) > Number(bArr[0]) && Number(aArr[2]) > Number(bArr[2])))
			return 1;
		if (!bArr[0].length || (Number(aArr[0]) < Number(bArr[0]) && Number(aArr[2]) < Number(bArr[2])))
			return -1;
		return 0;
	});
}

function convertTTRNumberToDay(key: string) {
	const oldAxisArray = key.split(/(-|>)+/);

	if (oldAxisArray[1] === ">") oldAxisArray[2] = ` ${Math.ceil(Number(oldAxisArray[2]))}`;
	else {
		oldAxisArray[0] = `${Math.ceil(Number(oldAxisArray[0]))}`;
		oldAxisArray[2] = `${Math.floor(Number(oldAxisArray[2]))}`;
	}

	return `${oldAxisArray.join("")} days`;
}

export function fixTTRBarChartAxisDisplayStyle(ttrData: ChartData): ChartData {
	let res: ChartData;

	res = ttrData.map((item) => {
		item.name = convertTTRNumberToDay(item.name);
		return item
	});

	res = sortByTTRKeys(res);

	return res;
}

export function fixTTRPredictionTableDisplayStyle(data: ObjectWithUnknownFields[]) {
	return data.map((item) => {
		item["Time to Resolve"] = convertTTRNumberToDay(item["Time to Resolve"] as string);
		return item;
	});
}

export function createChartDataFromObject(object: ObjectWithUnknownFields<number>): ChartData {
	return Object.entries(object).map(([name, value]) => {
		return {
			name,
			value
		}
	})
}
