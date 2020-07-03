import { HttpClient } from 'app/common/api/http-client';
import { HttpError, HttpValidationError } from 'app/common/types/http.types';
import { UserSignIn, UserSignUp } from 'app/common/types/user.types';

export class AuthApi {

	static baseUrl: string = 'auth';

	public static async signIn(signInData: UserSignIn) {
		try {
			return await HttpClient.post(this.baseUrl + '/signin/', signInData);
		} catch (e) {
			throw new HttpError(e);
		}
	}

	public static async signUp(signUpData: UserSignUp) {
		try {
			return await HttpClient.post(this.baseUrl + '/register/', signUpData);
		} catch (e) {
			throw new HttpValidationError(e, e['fields']);
		}
	}

	public static async getTeamList() {
		try {
			return await HttpClient.get(this.baseUrl + '/register/');
		} catch (e) {
			throw new HttpError(e);
		}
	}

}
