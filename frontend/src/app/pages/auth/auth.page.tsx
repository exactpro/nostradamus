import React from 'react';
import {Link, Redirect, Route, Switch} from "react-router-dom";

import {RootStore} from "app/common/types/store.types";
import {connect, ConnectedProps} from "react-redux";
import { getTeamList, userSignIn, userSignUp } from 'app/common/store/auth/thunks';

import Button, {ButtonStyled} from "app/common/components/button/button";
import {IconType} from "app/common/components/icon/icon";

import AuthPageSlider from "app/pages/auth/components/slider/auth-page-slider";
import SignIn from "app/pages/auth/components/forms/sign-in";
import SignUp from "app/pages/auth/components/forms/sign-up";

import './auth.page.scss';

import logoFull from "assets/images/logo-full.svg";
import authPageBackground from "assets/images/auth-page/auth-page-background.png";
import {RouterNames} from "app/common/types/router.types";

class AuthPage extends React.Component<Props> {

  componentDidMount() {
    this.props.getTeamList();
  }

  render() {
    const authPageStyle = {
      background:
        `url(${authPageBackground}) center,
        radial-gradient(92.42% 92.42% at 50% 100%, #1F5C7A 1.79%, #013047 100%)`
    };

    return (
      <article className="auth-page" style={authPageStyle}>
        <div className="auth-page__container">
          <div className="auth-page__logo">
            <img src={logoFull} alt="Nostradamus logo"/>
          </div>

          <div className="auth-page__content">
            <div className="auth-page__slider">
              <AuthPageSlider/>
            </div>


            <div className="auth-page__main">
              <Switch>
                <Route path={RouterNames.signIn} exact>
                  <Link to={RouterNames.signUp}>
                    <Button text="Register" icon={IconType.register} styled={ButtonStyled.Flat}
                            className="auth-page__change-mod-button"/>
                  </Link>

                  <SignIn className="auth-page__auth-form" signIn={this.props.userSignIn} status={this.props.status}/>
                </Route>

                <Route path={RouterNames.signUp} exact>
                  <Link to={RouterNames.signIn}>
                    <Button text="Sign In" icon={IconType.login} styled={ButtonStyled.Flat}
                            className="auth-page__change-mod-button"/>
                  </Link>

                  <SignUp className="auth-page__auth-form" signUp={this.props.userSignUp} status={this.props.status} teamList={this.props.teamList}/>
                </Route>

                <Route path={RouterNames.auth + RouterNames.rootPath} exact>
                  <Redirect to={RouterNames.signIn}/>
                </Route>

                <Route path={RouterNames.auth + RouterNames.rootPath + '*'}>
                  <Redirect to={RouterNames.rootPath}/>
                </Route>
              </Switch>
            </div>
          </div>
        </div>
      </article>
    );
  }
}

const mapStateToProps = ({auth}: RootStore) => ({
  status: auth.status,
  teamList: auth.teamList
});

const mapDispatchToProps = {
  userSignIn,
  userSignUp,
  getTeamList
};

const connector = connect(
  mapStateToProps,
  mapDispatchToProps
);

type PropsFromRedux = ConnectedProps<typeof connector>

type Props = PropsFromRedux & any;


export default connector(AuthPage);
