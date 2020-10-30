import React, { ReactElement } from "react";
import Card from "app/common/components/card/card";

import "./not-found.page.scss";

class NotFoundPage extends React.PureComponent {
	render(): ReactElement {
		return (
			<div className="not-found-page">
				<Card title="404" className="not-found-page__card">
					<h1>
						Sorry, page not found
						<span role="img" aria-label="Confused smile">
							😶
						</span>
					</h1>
				</Card>
			</div>
		);
	}
}

export default NotFoundPage;
