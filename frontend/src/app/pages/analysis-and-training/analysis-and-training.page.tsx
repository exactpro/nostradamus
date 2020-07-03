import Button, { ButtonStyled } from 'app/common/components/button/button';
import Card from 'app/common/components/card/card';
import { IconType } from 'app/common/components/icon/icon';
import { Timer } from 'app/common/functions/timer';
import { FilterFieldBase } from 'app/modules/filters/field/field-type';
import TrainingButton from 'app/modules/training-button/training-button';
import { applyAnalysisAndTrainingFilters } from 'app/common/store/analysis-and-training/thunks';
import MainStatistic from 'app/modules/main-statistic/main-statistic';
import { HttpStatus } from 'app/common/types/http.types';
import { RootStore } from 'app/common/types/store.types';
import DefectSubmission from 'app/modules/defect-submission/defect-submission';
import { Filters } from 'app/modules/filters/filters';
import FrequentlyUsedTerms from 'app/modules/frequently-used-terms/frequently-used-terms';
import Header from 'app/modules/header/header';
import SignificantTerms from 'app/modules/significant-terms/significant-terms';
import Statistic from 'app/modules/statistic/statistic';
import { getDashboardData } from 'app/common/store/analysis-and-training/thunks';
import { addToastWithAction } from 'app/modules/toasts-overlay/store/actions';
import { ToastStyle } from 'app/modules/toasts-overlay/store/types';

import defectSubmissionLoadingPreview from 'assets/images/defect-submission-loading-preview.png';
import frequentlyUsedTermsLoadingPreview from 'assets/images/frequently-used-terms-loading-preview.png';
import significantTermsLoadingPreview from 'assets/images/significant-terms-loading-preview.png';
import statisticsLoadingPreview from 'assets/images/statistics-loading-preview.png';
import filterLoadingPreview from 'assets/images/filter-loading-preview.png';
import { socket } from 'index';
import React from 'react';
import { connect, ConnectedProps } from 'react-redux';

import 'app/pages/analysis-and-training/analysis-and-training.page.scss';

import calculateData1 from 'assets/images/calculateData1.svg';
import calculateData2 from 'assets/images/calculateData2.svg';
import calculateData3 from 'assets/images/calculateData3.svg';

interface State {
	loadingStatus: number,
	filters: FilterFieldBase[]
}

const LOADING_TIME = 5 * 60 * 1000;

class AnalysisAndTrainingPage extends React.Component<PropsFromRedux, State> {

	interval: NodeJS.Timer | null = null;
	timer: Timer | null = null;

	imageForCalculating: string;

	readonly state: Readonly<State> = {
		loadingStatus: 0,
		filters: []
	};

	constructor(props: PropsFromRedux) {
		super(props);

		switch (Math.floor(Math.random() * 3)) {
			case 1:
				this.imageForCalculating = calculateData2;
				break;
			case 2:
				this.imageForCalculating = calculateData3;
				break;
			default:
				this.imageForCalculating = calculateData1;
				break;
		}
	}

	uploadDashboardData = () => {
		this.props.getDashboardData().then(filters => {
			if (filters) {
				this.setState({ filters: [...filters] });
			}
		});
	}

	componentDidMount(): void {
		this.uploadDashboardData();

		socket.startMonitor('message', (val) => {
			if (this.props.isCollectingFinished) {
				this.props.addToastWithAction('Data has been updated', ToastStyle.Info, [
					{
						buttonName: 'Load',
						callBack: () => { this.uploadDashboardData(); },
					},
				]);
			} else {
				document.location.reload();
			}
		});
	}

	componentDidUpdate(prevProps: Readonly<PropsFromRedux>, prevState: Readonly<State>, snapshot?: any): void {
		if (!this.props.isCollectingFinished && !this.interval) {
			this.interval = setInterval(() => {
				this.setState({
					...this.state,
					loadingStatus: this.state.loadingStatus < 100 ? this.state.loadingStatus + 1 : 100,
				});

				this.timer = new Timer(() => {
					if (this.interval) {
						clearInterval(this.interval);
					}
				}, LOADING_TIME);
			}, LOADING_TIME / 100);
		}
	}

	getSignificantTermsStatus = (): HttpStatus => {
		if ((this.props.status === HttpStatus.FINISHED) && !this.props.significant_terms.chosen_metric) {
			return HttpStatus.PREVIEW;
		}

		return this.props.status;
	};

	applyFilters = (filters: FilterFieldBase[]) => {
		this.setState({filters: []});
		this.props.applyFilters(filters).then(filters => {
			this.setState({ filters: [...filters] });
		});
	};

	resetFilters = () => {
		this.setState({filters: []});
		this.props.applyFilters([]).then(filters => {
			this.setState({ filters: [...filters] });
		});
	};

	render() {

		let blurIntensive = 10 - (this.state.loadingStatus / 100 * 9);
		let style = this.props.isCollectingFinished ? {} : { filter: `blur(${blurIntensive}px)` };

		return (
			<div className="at-page">
				<Header pageTitle="Analysis & Training">
					<MainStatistic className="at-page__main-statistic" />

					<TrainingButton className="at-page__train-button" />
				</Header>

				{
					!this.props.isCollectingFinished &&
          <div className="at-page__collecting-data collecting-data">
              <div className="collecting-data__message">
                  Making calculations… Please wait a few minutes
              </div>

              <img src={this.imageForCalculating} alt="Calculating Data" />

              <div className="collecting-data__loader">
                  <div className="collecting-data__loader-inner" style={{ width: this.state.loadingStatus + '%' }}>

                  </div>
              </div>
          </div>
				}

				<div className="at-page__content">
					<div className="at-page__column at-page__column_position_left" style={style}>

						<Card
							className="configuration-tab at-page__card"
							previewImage={filterLoadingPreview}
							status={this.props.status}
							isErrorAvailable
						>

							<div className="configuration-tab__container">

								<div className="configuration-tab__buttons">

									<Button
										className="configuration-tab__section-filters"
										text="Filter"
										icon={IconType.filter}
										styled={ButtonStyled.Flat}
										selected
									/>
								</div>

								{
									this.state.filters.length &&
                  <Filters
                      className="configuration-tab__filters"
                      filters={this.state.filters}
                      applyFilters={this.applyFilters}
                      resetFilters={this.resetFilters}
                  />
								}

							</div>
						</Card>

						<Card
							previewImage={statisticsLoadingPreview} title="Statistics"
							status={this.props.status}
							className="statistics at-page__card"
							hoverHeader
						>
							{this.props.statistic && <Statistic statistic={this.props.statistic} />}
						</Card>

					</div>

					<div className="at-page__column at-page__column_position_right" style={style}>
						<Card
							previewImage={defectSubmissionLoadingPreview} title="Defect Submission"
							status={this.props.status}
							className="defect-submission-card at-page__card"
						>
							<DefectSubmission />
						</Card>

						<Card
							previewImage={frequentlyUsedTermsLoadingPreview} title="Frequently Used Terms"
							status={this.props.frequentlyTermsList.length? this.props.status: HttpStatus.FAILED}
							className="frequently-used-terms at-page__card"
						>
							<FrequentlyUsedTerms frequentlyTermsList={this.props.frequentlyTermsList} />
						</Card>

						<Card
							previewImage={significantTermsLoadingPreview} title="Significant Terms"
							status={this.getSignificantTermsStatus()}
							className="at-page__significant-terms at-page__card" hoverHeader
						>
							<SignificantTerms />
						</Card>
					</div>
				</div>
			</div>
		);
	}
}

const mapStateToProps = (state: RootStore) => ({
	status: state.analysisAndTraining.analysisAndTraining.status,
	statistic: state.analysisAndTraining.analysisAndTraining.statistic,
	frequentlyTermsList: state.analysisAndTraining.analysisAndTraining.frequentlyTermsList,
	significant_terms: state.analysisAndTraining.significantTerms,
	isCollectingFinished: state.analysisAndTraining.analysisAndTraining.isCollectingFinished,
});

const mapDispatchToProps = {
	getDashboardData,
	addToastWithAction,
	applyFilters: applyAnalysisAndTrainingFilters,
};

const connector = connect(
	mapStateToProps,
	mapDispatchToProps,
);

type PropsFromRedux = ConnectedProps<typeof connector>

export default connector(AnalysisAndTrainingPage);
