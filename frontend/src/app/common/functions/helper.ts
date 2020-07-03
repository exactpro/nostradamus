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
