import { getDataFromLocalStorage } from "app/common/functions/local-storage";
import { User } from "app/common/types/user.types";

type EnhancedObject = { [key: string]: unknown };

class HttpClientConstructor {
	private tokenLocked = "";
	private readonly API_URL: string;

	private headers: Headers = new Headers({
		"Content-Type": "application/json",
	});

	constructor() {
		const user = getDataFromLocalStorage<User>("user");

		if (user) {
			this.token = user.token;
		}

		this.API_URL = "/api/";
	}

	private buildQueryParams = (params: EnhancedObject): string => {
		let queryParams = "?";

		const paramsNameList: string[] = Object.keys(params);

		paramsNameList.forEach((paramName: string, index) => {
			queryParams += `${paramName}=${encodeURIComponent(String(params[paramName]))}`;
			if (index !== paramsNameList.length - 1) {
				queryParams += "&";
			}
		});

		return queryParams;
	};

	public set token(token: string | null) {
		if (token) {
			this.headers.set("Authorization", `JWT ${token}`);
		} else {
			this.headers.delete("Authorization");
		}
		this.tokenLocked = token || "";
	}

	public get token() {
		return this.tokenLocked;
	}

	private async request(
		url: string,
		method: "POST" | "GET",
		query?: EnhancedObject | null,
		body?: Record<string, unknown>,
		outerUrl?: string
	): Promise<Response> {
		const fullUrl = (outerUrl || this.API_URL) + url + (query ? this.buildQueryParams(query) : "");

		return fetch(fullUrl, {
			method,
			headers: this.headers,
			body: JSON.stringify(body),
		});
	}

	public async get(url: string, query?: EnhancedObject, outerUrl?: string, fullResponse?: boolean) {
		const res: Response = await this.request(url, "GET", query, undefined, outerUrl);

		if (res.ok) {
			return fullResponse ? res : res.json();
		}
		throw (await res.json()).exception;
	}

	public async post(
		url: string,
		query?: any | null,
		body?: any,
		outerUrl?: string,
		fullResponse?: boolean
	) {
		const res: Response = await this.request(url, "POST", query, body, outerUrl);
		if (res.ok) {
			return fullResponse ? res : res.json();
		} 
		
		throw (await res.json()).exception;
	}
}

const HttpClient = new HttpClientConstructor();

export default HttpClient;
