import { DAProbabilitiesData } from "app/pages/description-assessment/description-assessment.page";
import { QAMetricsData } from "../store/qa-metrics/types";

export function isOneOf<T>(requiredElem: T, allElem: T[]): boolean {
	return allElem.findIndex((elem) => elem === requiredElem) > -1;
}

export function deleteExtraSpaces(str: string): string {
	return str.replace(/\s+/g, ' ').trim();
}

export function copyData(data: any){
  if(Array.isArray(data)) return [...data]
  else if (typeof data === "object") return {...data}
  else return data
}

export const isStrIncludesSubstr = (str: string, substr: string) => {
  return str.toUpperCase().includes(substr.toUpperCase());
}

export function caseInsensitiveStringCompare(a: string, b: string){
  return a.toUpperCase().trim().localeCompare(b.toUpperCase().trim());
}

// TTR processing functions 



function sortTTRKeys(oldKeys: Array<[string, unknown]>){
	oldKeys.sort((a,b)=>{
		let splitRegex = /(-| |>)+/;
		let aArr = a[0].split(splitRegex);
		let bArr = b[0].split(splitRegex);  
		
		if(!aArr[0].length || (Number(aArr[0]) > Number(bArr[0]) && Number(aArr[2]) > Number(bArr[2]))) return 1;
		else if (!bArr[0].length || (Number(aArr[0]) < Number(bArr[0]) && Number(aArr[2]) < Number(bArr[2]))) return -1;
		else return 0;
	})
}

function convertTTRNumberToDay(key: string){
	let oldAxisArray = key.split(/(-|>)+/);
		
	if(oldAxisArray[1] === ">") oldAxisArray[2] = ` ${Math.ceil(Number(oldAxisArray[2]))}`;
	else{
		oldAxisArray[0] = `${Math.ceil(Number(oldAxisArray[0]))}`;
		oldAxisArray[2] = `${Math.floor(Number(oldAxisArray[2]))}`;
	} 

	return oldAxisArray.join("")+" days";
}

export function fixTTRBarChartAxisDisplayStyle(oldTTRData: DAProbabilitiesData){
	
	let newTTRData: DAProbabilitiesData = {};
	let ttrKeyArr: Array<[string, unknown]> = [];

	Object.entries(oldTTRData).forEach(([key, val])=>{
		let oldAxisArray = convertTTRNumberToDay(key);
		ttrKeyArr.push([oldAxisArray, val]); 
	});

	sortTTRKeys(ttrKeyArr);
	newTTRData = Object.fromEntries(ttrKeyArr); 

	return newTTRData;
}

export function fixTTRPredictionTableDisplayStyle(data: QAMetricsData[]){
  return data.map(item=>{
      item["Time to Resolve"] = convertTTRNumberToDay(item["Time to Resolve"] as string); 
      return item
    });
}