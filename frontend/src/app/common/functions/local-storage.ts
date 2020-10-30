// TODO: refactor to class
export function getDataFromLocalStorage<T>(key: string): T | null {
	const storage = localStorage.getItem(key);
	return storage ? (JSON.parse(storage) as T) : null;
}

export function saveDataToLocalStorage(key: string, data: any): void {
	localStorage.setItem(key, JSON.stringify(data));
}

export function removeData(key: string): void {
	localStorage.removeItem(key);
}
