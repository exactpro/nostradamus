import React from 'react';
import cn from "classnames";

import Button from "app/common/components/button/button";
import {IconType} from "app/common/components/icon/icon";

import './forms.scss';
import {Team, UserSignUp} from "app/common/types/user.types";
import {HttpStatus} from "app/common/types/http.types";

interface SignUpProps {
  className?: string;
  signUp: (signUpData: UserSignUp) => void,
  status: HttpStatus
  teamList: Team[]
}

interface SignUpState {
  form: {
    isValid: boolean,
    value: UserSignUp
  }
}

class SignUp extends React.Component<SignUpProps, SignUpState> {

  state: Readonly<SignUpState> = {
    form: {
      isValid: false,
      value: {
        team: null,
        email: '',
        name: '',
        password: '',
      }
    }
  };

  changeField = (e: React.ChangeEvent<HTMLInputElement>) => {
    let state: SignUpState = this.state;
    const name: 'email' | 'name' | 'password' = e.target.name as ('email' | 'name' | 'password');

    state.form.value[name] = e.target.value;

    this.setState(state);
  };

  changeSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    let state: SignUpState = this.state;

    state.form.value.team = parseInt(e.target.value) > -1 ? parseInt(e.target.value) : null;

    this.setState(state);
  };

  formValidation = () => {
    let {isValid} = this.state.form;

    if (isValid !== this.checkFormIsValid()) {
      let state: SignUpState = this.state;
      state.form.isValid = !isValid;
      this.setState(state);
    }
  };

  checkFormIsValid = () => {
    let {team, email, name, password} = this.state.form.value;

    if (typeof team !== "number") {
      return false
    }

    // email contain @ and dot in domain and doesn't contain space symbols
    if (!email.match(/[a-zA-Z0-9_\-.]+@([a-zA-Z0-9_\-.]+\.)+[a-zA-Z0-9_\-.]{1,10}$/i)) {
      return false
    }

    // name have not only space symbols
    if (!name.match(/^[a-zA-Z0-9_.]+$/i)) {
      return false
    }

    if (password.length < 6 || !password.match(/^[a-zA-Z0-9_.\-]+$/i)) {
      return false;
    }

    return true;
  };

  formSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    this.props.signUp(this.state.form.value);
  };

  render() {

    return (
      <form className={cn("auth-form", this.props.className)} onChange={this.formValidation} onSubmit={this.formSubmit}>
        <h3 className="auth-form__title">
          Register
        </h3>

        <label className="auth-form__field">
          <span className="auth-form__label">Team</span>
          <select
            className="auth-form__input"
            id="sign-up_team"
            placeholder="Team"
            value={this.state.form.value.team || -1}
            onChange={this.changeSelect}
            name="team"
          >
            <option value={-1}>Select</option>
            {
              this.props.teamList.map((team: Team) => (
                <option key={team.id} value={team.id}>{team.name}</option>
              ))
            }
          </select>
        </label>

        <label className="auth-form__field">
          <span className="auth-form__label">E-mail</span>
          <input className="auth-form__input"
                 id="sign-up__e-mail"
                 type="text"
                 value={this.state.form.value.email}
                 onChange={this.changeField}
                 name="email"/>
        </label>

        <label className="auth-form__field">
          <span className="auth-form__label">Username</span>
          <input className="auth-form__input"
                 id="sign-up__username"
                 type="text"
                 value={this.state.form.value.name}
                 onChange={this.changeField}
                 name="name"/>
        </label>

        <label className="auth-form__field">
          <span className="auth-form__label">Password</span>
          <input className="auth-form__input"
                 id="sign-up__password"
                 type="password"
                 value={this.state.form.value.password}
                 onChange={this.changeField}
                 name="password"/>
        </label>

        <Button
          className="auth-form__submit-button"
          id="sign-up__submit"
          text="Send request" icon={IconType.check}
          disabled={!this.state.form.isValid || this.props.status === HttpStatus.LOADING}
          type="submit"/>
      </form>
    );
  }
}

export default SignUp;
