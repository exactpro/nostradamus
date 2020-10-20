import { checkCollectingIssuesFinished } from 'app/common/store/common/thunks';

import { RouterNames } from 'app/common/types/router.types';
import { RootStore } from 'app/common/types/store.types';

import Settings from 'app/modules/settings/settings';

import Sidebar from 'app/modules/sidebar/sidebar';
import VirtualAssistant from 'app/modules/virtual-assistant/virtual-assistant';
import AnalysisAndTrainingPage from 'app/pages/analysis-and-training/analysis-and-training.page';
import DescriptionAssessmentPage from 'app/pages/description-assessment/description-assessment.page';
import QAMetricsPage from 'app/pages/qa-metrics/qa-metrics.page';

import 'app/pages/root.page.scss';
import React from 'react';
import { connect, ConnectedProps } from 'react-redux';
import { Redirect, Route, Switch, withRouter } from 'react-router-dom';

const SidebarWithRouter = withRouter(props => <Sidebar {...props} />);

class RootPage extends React.Component<Props> {

	componentDidMount() {
		this.props.checkCollectingIssuesFinished();
	}

	render() {
		return (
			<div className="root-page">
				<SidebarWithRouter />
				<Settings />
				<VirtualAssistant />
				
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

const mapStateToProps = (store: RootStore) => ({});

const mapDispatchToProps = {
	checkCollectingIssuesFinished,
};

const connector = connect(
	mapStateToProps,
	mapDispatchToProps,
);

type PropsFromRedux = ConnectedProps<typeof connector>

type Props = PropsFromRedux;

export default connector(RootPage);
