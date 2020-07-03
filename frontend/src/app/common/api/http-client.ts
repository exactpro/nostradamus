import { getDataFromLocalStorage } from 'app/common/functions/local-storage';
import { User } from 'app/common/types/user.types';

type EnhancedObject = { [key: string]: any };

class HttpClientConstructor {

	private _token: string = '';
	private readonly API_URL: string;

	private headers: Headers = new Headers({
		'Content-Type': 'application/json',
	});

	constructor() {
		let user = getDataFromLocalStorage<User>('user');

		if (user) {
			this.token = user.token;
		}

		this.API_URL = '/api/';
	}

	private buildQueryParams(params: EnhancedObject): string {
		let queryParams = '?';

		const paramsNameList: string[] = Object.keys(params);

		paramsNameList.forEach((paramName: string, index) => {
			queryParams += paramName + '=' + encodeURIComponent(String(params[paramName]));
			if (index !== paramsNameList.length - 1) {
				queryParams += '&';
			}
		});

		return queryParams;
	}

	public set token(token: string | null) {
		if (token) {
			this.headers.set('Authorization', `JWT ${token}`);
		} else {
			this.headers.delete('Authorization');
		}
		this._token = token || '';
	}

	private async request(url: string, method: 'POST' | 'GET', query?: EnhancedObject | null, body?: Object, outerUrl?: string): Promise<Response> {

		let fullUrl = (outerUrl? outerUrl: this.API_URL) + url + (query ? this.buildQueryParams(query) : '');

		return await fetch(fullUrl, {
			method: method,
			headers: this.headers,
			body: JSON.stringify(body)
		});
	}


	public async get(url: string, query?: EnhancedObject, outerUrl?: string, fullResponse?: boolean) {
		const res: Response = await this.request(url, 'GET', query, outerUrl);

		if (res.ok) {
			return fullResponse ? res : res.json();
		} else {
			throw (await res.json())['exception'];
		}
	}

	public async post(url: string, query?: EnhancedObject | null, body?: EnhancedObject, outerUrl?: string, fullResponse?: boolean) {

		const res: Response = await this.request(url, 'POST', query, body, outerUrl);

		if (res.ok) {
			return fullResponse ? res : res.json();
		} else {
			throw (await res.json())['exception'];
		}
	}

}

export const HttpClient = new HttpClientConstructor();
