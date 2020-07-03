import React from 'react';
import cn from "classnames";

import Button from "app/common/components/button/button";
import {IconType} from "app/common/components/icon/icon";
import {UserSignIn} from "app/common/types/user.types"; 

import './forms.scss';
import {HttpStatus} from "app/common/types/http.types";

interface SignInProps {
  className?: string;
  signIn: (signInData: UserSignIn) => void,
  status: HttpStatus
}

interface SignInState {
  form: {
    isValid: boolean,
    value: UserSignIn
  }
}

class SignIn extends React.Component<SignInProps, SignInState> {

  state: Readonly<SignInState> = {
    form: {
      isValid: false,
      value: {
        credentials: '',
        password: '',
      }
    }
  };

  changeField = (e: React.ChangeEvent<HTMLInputElement>) => {
    let state: SignInState = this.state;
    const name: 'credentials' | 'password' = e.target.name as ('credentials' | 'password');

    state.form.value[name] = e.target.value;

    this.setState(state);
  };

  formValidation = () => {
    let { isValid } = this.state.form;

    if (isValid !== this.checkFormIsValid()) {
      let state: SignInState = this.state;
      state.form.isValid = !isValid;
      this.setState(state);
    }
  };

  checkFormIsValid = () => {
    let { credentials, password } = this.state.form.value;

    // TODO: dirty code
    if (credentials.length < 1 || credentials.length > 254 || !credentials.match(/\S/i)) {
      return false;
    }

    if (password.length < 6 || !password.match(/\S/i)) {
      return false;
    }

    return true;
  };

  formSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    this.props.signIn(this.state.form.value);
  };

  render() {

    return (
      <form className={cn("auth-form", this.props.className)} onChange={this.formValidation} onSubmit={this.formSubmit}>
        <h3 className="auth-form__title">
          Sign in
        </h3>
        <label className="auth-form__field">
        <span className="auth-form__label">E-mail or Username</span>
        <input className="auth-form__input"
                 id="sign-in__credentials"
                 type="text"
                 value={this.state.form.value.credentials}
                 onChange={this.changeField}
                 name="credentials"
                 spellCheck="false"
          />
        </label>

        <label className="auth-form__field">
          <span className="auth-form__label">Password</span>
          <input className="auth-form__input"
                 id="sign-in__password"
                 type="password"
                 value={this.state.form.value.password}
                 onChange={this.changeField}
                 name="password"/>
        </label>

        <Button
          className="auth-form__submit-button"
          id="sign-in__submit"
          text="Submit" icon={IconType.check}
          disabled={!this.state.form.isValid || this.props.status === HttpStatus.LOADING}
          type="submit"/>
      </form>
    );
  }
}

export default SignIn;
