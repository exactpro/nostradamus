import { SocketEventType } from "app/common/api/sockets";
import Button, { ButtonStyled } from "app/common/components/button/button";
import Card from "app/common/components/card/card";
import { IconType } from "app/common/components/icon/icon";
import Tooltip, { TooltipPosition } from "app/common/components/tooltip/tooltip";
import { Timer } from "app/common/functions/timer";
import {
	updateFilters,
	uploadDashboardData,
	uploadDefectSubmission,
	uploadSignificantTermsList,
} from "app/common/store/analysis-and-training/thunks";
import { checkIssuesStatus } from "app/common/store/common/thunks";
import { checkIssuesExist } from "app/common/store/common/utils";
import { RootStore } from "app/common/types/store.types";
import DefectSubmission from "app/modules/defect-submission/defect-submission";
import { FilterFieldBase } from "app/modules/filters/field/field-type";
import { Filters } from "app/modules/filters/filters";
import FrequentlyUsedTerms from "app/modules/frequently-used-terms/frequently-used-terms";
import Header from "app/modules/header/header";
import MainStatistic from "app/modules/main-statistic/main-statistic";
import SignificantTerms from "app/modules/significant-terms/significant-terms";
import Statistic from "app/modules/statistic/statistic";
import {
	addToast,
	addToastWithAction,
	removeToastByOuterId,
} from "app/modules/toasts-overlay/store/actions";
import { ToastStyle } from "app/modules/toasts-overlay/store/types";
import TrainingButton from "app/modules/training-button/training-button";

import "app/pages/analysis-and-training/analysis-and-training.page.scss";

import calculateData1 from "assets/images/calculateData1.svg";
import calculateData2 from "assets/images/calculateData2.svg";
import calculateData3 from "assets/images/calculateData3.svg";

import defectSubmissionLoadingPreview from "assets/images/defect-submission-loading-preview.png";
import filterLoadingPreview from "assets/images/filter-loading-preview.png";
import frequentlyUsedTermsLoadingPreview from "assets/images/frequently-used-terms-loading-preview.png";
import significantTermsLoadingPreview from "assets/images/significant-terms-loading-preview.png";
import statisticsLoadingPreview from "assets/images/statistics-loading-preview.png";
import { socket } from "index";
import React from "react";
import { connect, ConnectedProps } from "react-redux";

interface State {
	loadingStatus: number;
}

const LOADING_TIME = 5 * 60 * 1000;

class AnalysisAndTrainingPage extends React.Component<PropsFromRedux, State> {
	interval: NodeJS.Timer | null = null;
	timer: Timer | null = null;
	isComponentMounted = false;
	updateDataToastID = 0;

	imageForCalculating: string;

	readonly state: Readonly<State> = {
		loadingStatus: 0,
	};

	constructor(innerProps: PropsFromRedux) {
		super(innerProps);

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

	componentDidMount(): void {
		this.isComponentMounted = true;

		this.startSocket();

		if (!this.props.totalStatistic) {
			this.props.uploadDashboardData();
		}
	}

	componentDidUpdate(): void {
		if (this.props.isLoadedIssuesStatus && !this.props.isIssuesExist && !this.interval) {
			this.interval = setInterval(() => {
				this.setState((state) => ({
					loadingStatus: state.loadingStatus < 100 ? state.loadingStatus + 1 : 100,
				}));

				this.timer = new Timer(() => {
					if (this.interval) {
						clearInterval(this.interval);
					}
				}, LOADING_TIME);
			}, LOADING_TIME / 100);
		}
	}

	componentWillUnmount = () => {
		if (this.updateDataToastID) {
			this.props.removeToastByOuterId(this.updateDataToastID);
		}

		socket.unsubscribe(SocketEventType.updateCountIssues);
	};

	startSocket = () => {
		socket.subscribeToEvent(SocketEventType.updateCountIssues, () => {
			checkIssuesExist().then((isIssuesExist) => {
				if (!isIssuesExist) {
					this.props.checkIssuesStatus();
					this.props.uploadDashboardData();
				} else {
					this.updateDataToastID += 1;

					const toast = {
						message: "Data has been updated",
						style: ToastStyle.Info,
						buttons: [{ buttonName: "Load", callBack: this.props.uploadDashboardData }],
						outerId: this.updateDataToastID,
					};

					this.props.addToastWithAction(toast);
				}
			});
		});
	};

	applyFilters = (filters: FilterFieldBase[]) => {
		this.props.updateFilters(filters);
	};

	resetFilters = () => {
		this.props.updateFilters([]);
	};

	render() {
		const { state } = this;

		const showCoffeemaker =
			!this.props.totalStatistic && this.props.isLoadedIssuesStatus && !this.props.isIssuesExist;

		const blurIntensive = 10 - (state.loadingStatus / 100) * 9;
		const style = showCoffeemaker ? { filter: `blur(${blurIntensive}px)` } : {};

		return (
			<div className="at-page">
				<Header pageTitle="Analysis & Training">
					<div className="at-page__header-container">
						<MainStatistic
							className="at-page__main-statistic"
							statistic={this.props.totalStatistic}
						/>

						<div className="at-page__train-panel">
							<TrainingButton className="at-page__train-button" />

							<Tooltip
								message="Training is performed using closed bugs only"
								position={TooltipPosition.bottom}
							>
								<p className="at-page__explanatory-mark">?</p>
							</Tooltip>
						</div>
					</div>
				</Header>

				{showCoffeemaker && (
					<div className="at-page__collecting-data collecting-data">
						<div className="collecting-data__message">
							Making calculations… Please wait a few minutes
						</div>

						<img src={this.imageForCalculating} alt="Calculating Data" />

						<div className="collecting-data__loader">
							<div
								className="collecting-data__loader-inner"
								style={{ width: `${state.loadingStatus}%` }}
							/>
						</div>
					</div>
				)}

				<div className="at-page__content">
					<div className="at-page__column at-page__column_position_left" style={style}>
						<Card
							className="configuration-tab at-page__card at-page__card_filter"
							previewImage={filterLoadingPreview}
							status={this.props.statuses.filter}
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

								<Filters
									className="configuration-tab__filters"
									filters={this.props.filters}
									applyFilters={this.applyFilters}
									resetFilters={this.resetFilters}
								/>
							</div>
						</Card>

						<Card
							previewImage={statisticsLoadingPreview}
							title="Statistics"
							status={this.props.statuses.statistic}
							className="statistics at-page__card"
							hoverHeader
						>
							<Statistic statistic={this.props.statistic} />
						</Card>
					</div>

					<div className="at-page__column at-page__column_position_right" style={style}>
						<Card
							previewImage={defectSubmissionLoadingPreview}
							title="Defect Submission"
							status={this.props.statuses.defectSubmission}
							className="defect-submission-card at-page__card"
						>
							<DefectSubmission
								defectSubmission={this.props.defectSubmission}
								onChangePeriod={this.props.uploadDefectSubmission}
							/>
						</Card>

						<Card
							previewImage={frequentlyUsedTermsLoadingPreview}
							title="Frequently Used Terms"
							status={this.props.statuses.frequentlyTerms}
							className="frequently-used-terms at-page__card"
							warningMessage={this.props.warnings.frequentlyTerms}
						>
							<FrequentlyUsedTerms frequentlyTermsList={this.props.frequentlyTerms} />
						</Card>

						<Card
							previewImage={significantTermsLoadingPreview}
							title="Significant Terms"
							status={this.props.statuses.significantTerms}
							className="at-page__significant-terms at-page__card"
							warningMessage={this.props.warnings.significantTerms}
							hoverHeader
						>
							<SignificantTerms
								status={this.props.statuses.significantTerms}
								onChangeMetric={this.props.uploadSignificantTermsList}
								metrics={this.props.significantTerms.metrics}
								chosen_metric={this.props.significantTerms.chosen_metric}
								terms={this.props.significantTerms.terms}
							/>
						</Card>
					</div>
				</div>
			</div>
		);
	}
}

const mapStateToProps = (store: RootStore) => ({
	isIssuesExist: store.common.isIssuesExist,
	isLoadedIssuesStatus: store.common.isLoadedIssuesStatus,
	statuses: store.analysisAndTraining.statuses,
	significantTerms: store.analysisAndTraining.significantTerms,
	frequentlyTerms: store.analysisAndTraining.frequentlyTerms,
	defectSubmission: store.analysisAndTraining.defectSubmission,
	statistic: store.analysisAndTraining.statistic,
	filters: store.analysisAndTraining.filters,
	totalStatistic: store.analysisAndTraining.totalStatistic,
	warnings: store.analysisAndTraining.warnings,
});

const mapDispatchToProps = {
	addToastWithAction,
	addToast,
	removeToastByOuterId,
	uploadDashboardData,
	uploadSignificantTermsList,
	uploadDefectSubmission,
	updateFilters,
	checkIssuesStatus,
};

const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

export default connector(AnalysisAndTrainingPage);
