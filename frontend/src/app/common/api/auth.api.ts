import HttpClient from "app/common/api/http-client";
import {
	HttpError,
	HTTPValidationError
} from "app/common/types/http.types";
import { UserSignIn, UserSignUp } from "app/common/types/user.types";

export class AuthApi {
	static baseUrl = "auth";

	public static async getUserId(token: string) {
		try {
			return await HttpClient.get(`${this.baseUrl}/verify_token/`, { token });
		} catch (e) {
			throw new HttpError(e);
		}
	}

	public static async signIn(signInData: UserSignIn) {
		try {
			return await HttpClient.post(`${this.baseUrl}/sign_in/`, null, signInData);
		} catch (e) {
			throw new HttpError(e);
		}
	}

	public static async signUp(signUpData: UserSignUp) {
		try {
			return await HttpClient.post(`${this.baseUrl}/register/`, null, signUpData);
		} catch (e) {
			throw new HTTPValidationError(e);
		}
	}
}
