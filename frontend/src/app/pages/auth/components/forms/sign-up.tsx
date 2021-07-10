import React, { ReactElement } from "react";
import cn from "classnames";

import Button from "app/common/components/button/button";
import { IconType } from "app/common/components/icon/icon";

import "./forms.scss";
import { UserSignUp } from "app/common/types/user.types";
import { HttpStatus } from "app/common/types/http.types";

interface SignUpProps {
	className?: string;
	signUp: (signUpData: UserSignUp) => void;
	status: HttpStatus;
}

interface SignUpState {
	form: {
		isValid: boolean;
		value: UserSignUp;
	};
}

class SignUp extends React.Component<SignUpProps, SignUpState> {
	constructor(props: SignUpProps) {
		super(props);

		this.state = {
			form: {
				isValid: false,
				value: {
					email: "",
					name: "",
					password: "",
				},
			},
		};
	}

	changeField = (e: React.ChangeEvent<HTMLInputElement>) => {
		const { form } = this.state;
		const name: "email" | "name" | "password" = e.target.name as "email" | "name" | "password";

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
		const { email, name, password } = this.state.form.value;

		// email contain @ and dot in domain and doesn't contain space symbols
		if (!/[a-zA-Z0-9_\-.]+@([a-zA-Z0-9_\-.]+\.)+[a-zA-Z0-9_\-.]{1,10}$/i.exec(email)) {
			return false;
		}

		// name have not only space symbols
		if (!/^[a-zA-Z0-9_.]+$/i.exec(name)) {
			return false;
		}

		if (password.length < 6) {
			return false;
		}

		return true;
	};

	formSubmit = (e: React.FormEvent): void => {
		e.preventDefault();

		this.props.signUp(this.state.form.value);
	};

	render(): ReactElement {
		const { state, props } = this;

		return (
			<form
				className={cn("auth-form", "auth-form_type_sign-up", props.className)}
				onChange={this.formValidation}
				onSubmit={this.formSubmit}
			>
				<h3 className="auth-form__title">Register</h3>

				<label className="auth-form__field" htmlFor="sign-up__e-mail">
					<span className="auth-form__label">E-mail</span>
					<input
						className="auth-form__input"
						id="sign-up__e-mail"
						type="text"
						value={state.form.value.email}
						onChange={this.changeField}
						name="email"
					/>
				</label>

				<label className="auth-form__field" htmlFor="sign-up__username">
					<span className="auth-form__label">Username</span>
					<input
						className="auth-form__input"
						id="sign-up__username"
						type="text"
						value={state.form.value.name}
						onChange={this.changeField}
						name="name"
					/>
				</label>

				<label className="auth-form__field" htmlFor="sign-up__password">
					<span className="auth-form__label">Password</span>
					<input
						className="auth-form__input"
						id="sign-up__password"
						type="password"
						value={state.form.value.password}
						onChange={this.changeField}
						name="password"
					/>
				</label>

				<Button
					className="auth-form__submit-button"
					id="sign-up__submit"
					text="Send request"
					icon={IconType.check}
					disabled={!state.form.isValid || props.status === HttpStatus.LOADING}
					type="submit"
				/>
			</form>
		);
	}
}

export default SignUp;
