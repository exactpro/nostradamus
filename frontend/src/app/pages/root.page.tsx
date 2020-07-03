import AnalysisAndTrainingPage from 'app/pages/analysis-and-training/analysis-and-training.page';
import DescriptionAssessmentPage from 'app/pages/description-assessment/description-assessment.page';
import QAMetricsPage from 'app/pages/qa-metrics/qa-metrics.page';
import React from 'react';
import { Redirect, Route, Switch, withRouter } from 'react-router-dom';

import { RouterNames } from 'app/common/types/router.types';

import Sidebar from 'app/modules/sidebar/sidebar';

import Settings from "app/modules/settings/settings";
import VirtualAssistant from "app/modules/virtual-assistant/virtual-assistant";

import 'app/pages/root.page.scss';

const SidebarWithRouter = withRouter(props => <Sidebar {...props} />);

class RootPage extends React.Component {

	render() {
		return (
			<div className="root-page">
				<SidebarWithRouter />
        <Settings/>
        <VirtualAssistant/>

				<Settings />
				<div className="root-page__content">
					<article>
						<Switch>
							<Route path={RouterNames.mainApp} exact>
								<Redirect to={RouterNames.analysisAndTraining} />
							</Route>

							<Route path={RouterNames.analysisAndTraining} exact>
								<AnalysisAndTrainingPage />
							</Route>

							<Route path={RouterNames.descriptionAssessment} exact>
								<DescriptionAssessmentPage />
							</Route>

							<Route path={RouterNames.qaMetrics} exact>
								<QAMetricsPage />
							</Route>

							<Route path={RouterNames.mainApp + '*'}>
								<Redirect to={RouterNames.notFound} />
							</Route>
						</Switch>
					</article>
				</div>
			</div>
		);
	}
}

export default RootPage;
