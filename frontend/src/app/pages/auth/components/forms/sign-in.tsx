import React from "react";
import cn from "classnames";

import Button from "app/common/components/button/button";
import { IconType } from "app/common/components/icon/icon";
import { UserSignIn } from "app/common/types/user.types";

import "./forms.scss";
import { HttpStatus } from "app/common/types/http.types";

interface SignInProps {
	className?: string;
	signIn: (signInData: UserSignIn) => void;
	status: HttpStatus;
}

interface SignInState {
	form: {
		isValid: boolean;
		value: UserSignIn;
	};
}

class SignIn extends React.Component<SignInProps, SignInState> {
	constructor(props: SignInProps) {
		super(props);

		this.state = {
			form: {
				isValid: false,
				value: {
					credentials: "",
					password: "",
				},
			},
		};
	}

	changeField = (e: React.ChangeEvent<HTMLInputElement>) => {
		const { form } = this.state;
		const name: "credentials" | "password" = e.target.name as "credentials" | "password";

		form.value[name] = e.target.value;

		this.setState({ form });
	};

	formValidation = () => {
		const { isValid } = this.state.form;

		if (isValid !== this.checkFormIsValid()) {
			this.setFormValidationStatus(!isValid);
		}
	};

	setFormValidationStatus = (newStatus: boolean) => {
		const { form } = this.state;
		form.isValid = newStatus;
		this.setState({ form });
	};

	checkFormIsValid = () => {
		const { credentials, password } = this.state.form.value;

		// TODO: dirty code
		if (credentials.length < 1 || credentials.length > 254 || !/\S/i.exec(credentials)) {
			return false;
		}

		if (password.length < 6) {
			return false;
		}

		return true;
	};

	formSubmit = (e: React.FormEvent): void => {
		e.preventDefault();

		this.props.signIn(this.state.form.value);
	};

	render() {
		const { state, props } = this;

		return (
			<form
				className={cn("auth-form", "auth-form_type_sign-in", this.props.className)}
				onChange={this.formValidation}
				onSubmit={this.formSubmit}
			>
				<h3 className="auth-form__title">Sign in</h3>
				<label className="auth-form__field">
					<span className="auth-form__label">E-mail or Username</span>
					<input
						className="auth-form__input"
						id="sign-in__credentials"
						type="text"
						value={this.state.form.value.credentials}
						onChange={this.changeField}
						name="credentials"
						spellCheck="false"
					/>
				</label>

				<label className="auth-form__field" htmlFor="sign-in__password">
					<span className="auth-form__label">Password</span>
					<input
						className="auth-form__input"
						id="sign-in__password"
						type="password"
						value={state.form.value.password}
						onChange={this.changeField}
						name="password"
					/>
				</label>

				<Button
					className="auth-form__submit-button"
					id="sign-in__submit"
					text="Submit"
					icon={IconType.check}
					disabled={!state.form.isValid || props.status === HttpStatus.LOADING}
					type="submit"
				/>
			</form>
		);
	}
}

export default SignIn;
