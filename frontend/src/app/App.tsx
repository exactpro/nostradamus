import ToastsOverlay from "app/modules/toasts-overlay/toasts-overlay";
import React from "react";
import "./App.scss";

import RootPage from "app/pages/root.page";

import { connect, ConnectedProps } from "react-redux";
import { history } from "app/common/store/configureStore";
import AuthPage from "app/pages/auth/auth.page";
import { Redirect, Route, Switch } from "react-router-dom";
import { ConnectedRouter } from "connected-react-router";
import { RouterNames } from "app/common/types/router.types";
import NotFoundPage from "app/pages/not-found/not-found.page";
import { RootStore } from "app/common/types/store.types";

class App extends React.PureComponent<Props> {
	render() {
		const { user } = this.props;

		return (
			<div className="app-container">
				<ConnectedRouter history={history}>
					<Switch>
						<Route path={RouterNames.rootPath} exact>
							<Redirect to={RouterNames.mainApp} />
						</Route>

						<Route path={`${RouterNames.mainApp}*`} exact>
							{user ? <RootPage /> : <Redirect to={RouterNames.signIn} />}
						</Route>

						<Route path={`${RouterNames.auth}*`} exact>
							{!user ? <AuthPage /> : <Redirect to={RouterNames.mainApp} />}
						</Route>

						<Route path={RouterNames.notFound} exact>
							<NotFoundPage />
						</Route>

						<Route path="*">
							<Redirect to={RouterNames.notFound} />
						</Route>
					</Switch>
				</ConnectedRouter>

				<ToastsOverlay />
			</div>
		);
	}
}

const mapStateToProps = (store: RootStore) => ({
	user: store.auth.user,
});

const connector = connect(mapStateToProps);

type Props = ConnectedProps<typeof connector>;

export default connector(App);
