import React, { ReactElement } from "react";

import "./header.scss";

interface HeaderProps {
	pageTitle: string;
}

class Header extends React.PureComponent<HeaderProps> {
	render(): ReactElement {
		const { props } = this;

		return (
			<header className="header">
				<h1 className="header__title">{props.pageTitle}</h1>

				{props.children}
			</header>
		);
	}
}

export default Header;
