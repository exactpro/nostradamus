import { AuthApi } from "app/common/api/auth.api";
import HttpClient from "app/common/api/http-client";
import { deleteExtraSpaces } from "app/common/functions/helper";
import { saveDataToLocalStorage } from "app/common/functions/local-storage";
import { deleteUser, setStatus, setUser } from "app/common/store/auth/actions";
import { resetCommonStatuses } from "app/common/store/common/actions";
import { clearQAMetricsData } from "app/common/store/qa-metrics/actions";
import { clearSettingsData } from "app/common/store/settings/thunks";
import { clearMessages } from "app/common/store/virtual-assistant/actions";
import {
	HTTPFieldValidationError,
	HttpStatus
} from "app/common/types/http.types";
import { RouterNames } from "app/common/types/router.types";
import { User, UserSignIn, UserSignUp } from "app/common/types/user.types";
import { addToast } from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";
import { push } from "connected-react-router";

export const verifyToken = (token: string) => {
	return async (dispatch: any) => {
		try {
			await AuthApi.getUserId(token);
		} catch (e) {
			dispatch(logout());
			dispatch(addToast(e.detail, ToastStyle.Error));
			return;
		}
	};
};

export const userSignIn = (signInData: UserSignIn) => {
	return async (dispatch: any) => {
		dispatch(setStatus(HttpStatus.LOADING));
		let user: User;
		try {
			user = await AuthApi.signIn(signInData);
		} catch (e) {
			dispatch(addToast(e.detail, ToastStyle.Error));
			dispatch(setStatus(HttpStatus.FAILED));
			return;
		}
		saveDataToLocalStorage("user", user);
		HttpClient.token = user.token;
		dispatch(setUser(user));
		dispatch(push(RouterNames.analysisAndTraining));
		dispatch(addToast("Logged in successfully", ToastStyle.Success));
		dispatch(setStatus(HttpStatus.FINISHED));
	};
};

export const userSignUp = (signUpData: UserSignUp) => {
	return async (dispatch: any) => {
		dispatch(setStatus(HttpStatus.LOADING));
		signUpData.name = deleteExtraSpaces(signUpData.name);
		try {
			await AuthApi.signUp(signUpData);
		} catch (e) {
			e.fields.forEach((field: HTTPFieldValidationError) => {
				field.errors.forEach(validationError => {
					dispatch(addToast(validationError , ToastStyle.Error));
				});
			});

			dispatch(setStatus(HttpStatus.FAILED));
			return;
		}
		dispatch(addToast("Registration completed successfully", ToastStyle.Success));
		dispatch(push(RouterNames.signIn));
		dispatch(setStatus(HttpStatus.FINISHED));
	};
};

export const logout = () => {
	return async (dispatch: any) => {
		HttpClient.token = '';

		dispatch(deleteUser());
		dispatch(clearQAMetricsData());
		dispatch(clearSettingsData());
		dispatch(clearMessages());
		dispatch(resetCommonStatuses());
		dispatch(push(RouterNames.auth));
	};
};
