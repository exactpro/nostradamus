import { AnalysisAndTrainingApi } from "app/common/api/analysis-and-training.api";
import Button, { ButtonStyled } from "app/common/components/button/button";
import Card from "app/common/components/card/card";
import { IconType } from "app/common/components/icon/icon";
import { Timer } from "app/common/functions/timer";
import { setCollectingDataStatus } from "app/common/store/settings/actions";
import {
	AnalysisAndTrainingDefectSubmission,
	AnalysisAndTrainingStatistic,
	DefectSubmissionData,
	SignificantTermsData,
} from "app/common/types/analysis-and-training.types";
import { HttpStatus } from "app/common/types/http.types";
import DefectSubmission from "app/modules/defect-submission/defect-submission";
import { FilterFieldBase } from "app/modules/filters/field/field-type";
import { checkFieldIsFilled } from "app/modules/filters/field/field.helper-function";
import { Filters, FiltersPopUp } from "app/modules/filters/filters";
import FrequentlyUsedTerms from "app/modules/frequently-used-terms/frequently-used-terms";
import Header from "app/modules/header/header";
import MainStatistic, { MainStatisticData } from "app/modules/main-statistic/main-statistic";
import SignificantTerms from "app/modules/significant-terms/significant-terms";
import { Terms } from "app/modules/significant-terms/store/types";
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
	filters: FilterFieldBase[];
	totalStatistic: MainStatisticData | undefined;
	frequentlyTerms: string[];
	isCollectingFinished: boolean;
	statistic: AnalysisAndTrainingStatistic | undefined;
	significantTerms: SignificantTermsData;
	defectSubmission: DefectSubmissionData;
	statuses: {
		[key: string]: HttpStatus;
		filter: HttpStatus;
		frequentlyTerms: HttpStatus;
		defectSubmission: HttpStatus;
		statistic: HttpStatus;
		significantTerms: HttpStatus;
	};
	warnings: {
		frequentlyTerms: string;
	};
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
		filters: [],
		totalStatistic: undefined,
		frequentlyTerms: [],
		isCollectingFinished: true,
		statistic: undefined,
		significantTerms: {
			metrics: [],
			chosen_metric: null,
			terms: {},
		},
		defectSubmission: {
			data: undefined,
			activePeriod: undefined,
		},
		statuses: {
			filter: HttpStatus.PREVIEW,
			frequentlyTerms: HttpStatus.PREVIEW,
			defectSubmission: HttpStatus.PREVIEW,
			statistic: HttpStatus.PREVIEW,
			significantTerms: HttpStatus.PREVIEW,
		},
		warnings: {
			frequentlyTerms: "",
		},
	};

	constructor(innerProps: PropsFromRedux) {
		super(innerProps);

		const { props, state } = this;
		props.setCollectingDataStatus(state.isCollectingFinished);

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
		const { isCollectingFinished } = this.state;

		this.uploadTotalStatistic().then((filtered) => {
			if (isCollectingFinished) {
				if (filtered) {
					this.uploadDashboardData("full");
				} else {
					this.uploadDashboardData("filters");
				}
			}
		});

		this.startSocket();
	}

	componentDidUpdate(): void {
		const { isCollectingFinished } = this.state;

		if (!isCollectingFinished && !this.interval) {
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
		const { props } = this;

		this.isComponentMounted = false;
		if (this.updateDataToastID) {
			props.removeToastByOuterId(this.updateDataToastID);
		}
	};

	uploadDashboardData = (typeUpload: "full" | "data" | "filters" = "data") => {
		if (typeUpload === "full" || typeUpload === "filters") {
			this.uploadFilters();
		}

		if (typeUpload === "full" || typeUpload === "data") {
			this.uploadFrequentlyTerms();
			this.uploadStatistic();
			this.uploadDefectSubmission();
			this.uploadSignificantTermsData();
		}
	};

	startSocket = () => {
		const { props, state } = this;

		socket.startMonitor("message", () => {
			if (state.isCollectingFinished && this.isComponentMounted) {
				this.updateDataToastID += 1;
				props.addToastWithAction(
					"Data has been updated",
					ToastStyle.Info,
					[
						{
							buttonName: "Load",
							callBack: () => {
								this.uploadTotalStatistic().then((_) => this.uploadDashboardData("full"));
							},
						},
					],
					this.updateDataToastID
				);
			} else if (!state.isCollectingFinished) {
				document.location.reload();
			}
		});
	};

	validateUploadData = (data: any, cardName: string) => {
		if (!(data && Object.keys(data).length)) {
			this.setState((state) => ({
				statuses: { ...state.statuses, [cardName]: HttpStatus.PREVIEW },
			}));
			return true;
		}
		return false;
	};

	uploadSignificantTermsData = async () => {
		this.setState((state) => ({
			statuses: { ...state.statuses, significantTerms: HttpStatus.LOADING },
		}));

		let significant_terms: SignificantTermsData;

		try {
			significant_terms = (await AnalysisAndTrainingApi.getSignificantTermsData())
				.significant_terms;
		} catch (e) {
			this.setState((state) => ({
				statuses: { ...state.statuses, significantTerms: HttpStatus.FAILED },
			}));
			return;
		}

		if (this.validateUploadData(significant_terms, "significantTerms")) return;

		this.setState((state) => ({
			statuses: { ...state.statuses, significantTerms: HttpStatus.FINISHED },
			significantTerms: {
				metrics: [...significant_terms.metrics],
				chosen_metric: significant_terms.chosen_metric,
				terms: { ...significant_terms.terms },
			},
		}));
	};

	uploadSignificantTermsList = async (metric: string) => {
		this.setState((state) => ({
			statuses: { ...state.statuses, significantTerms: HttpStatus.LOADING },
			significantTerms: {
				...state.significantTerms,
				chosen_metric: metric,
			},
		}));

		let significant_terms: Terms;

		try {
			significant_terms = (await AnalysisAndTrainingApi.getSignificantTermsList(metric))
				.significant_terms;
		} catch (e) {
			this.setState((state) => ({
				statuses: { ...state.statuses, significantTerms: HttpStatus.FAILED },
			}));
			return;
		}

		if (this.validateUploadData(significant_terms, "significantTerms")) return;

		this.setState((state) => ({
			statuses: { ...state.statuses, significantTerms: HttpStatus.FINISHED },
			significantTerms: {
				...state.significantTerms,
				terms: { ...significant_terms },
			},
		}));
	};

	uploadDefectSubmission = async (period?: string) => {
		this.setState((state) => ({
			defectSubmission: {
				...state.defectSubmission,
				activePeriod: period,
			},
			statuses: { ...state.statuses, defectSubmission: HttpStatus.LOADING },
		}));

		let defectSubmission: AnalysisAndTrainingDefectSubmission;

		try {
			defectSubmission = await AnalysisAndTrainingApi.getDefectSubmission(period);
		} catch (e) {
			this.setState((state) => ({
				statuses: { ...state.statuses, defectSubmission: HttpStatus.FAILED },
			}));
			return;
		}

		if (this.validateUploadData(defectSubmission, "defectSubmission")) return;

		this.setState((state) => ({
			defectSubmission: {
				data: defectSubmission,
				activePeriod: defectSubmission!.period,
			},
			statuses: { ...state.statuses, defectSubmission: HttpStatus.FINISHED },
		}));
	};

	uploadFrequentlyTerms = async () => {
		this.setState((state) => ({
			statuses: { ...state.statuses, frequentlyTerms: HttpStatus.LOADING },
		}));

		let body: any;

		try {
			body = await AnalysisAndTrainingApi.getFrequentlyTerms();
		} catch (e) {
			this.setState((state) => ({
				statuses: { ...state.statuses, frequentlyTerms: HttpStatus.FAILED },
			}));
			return;
		}

		if (this.validateUploadData(body, "frequentlyTerms")) return;

		if (body.frequently_terms) {
			this.setState((state) => ({
				frequentlyTerms: [...body.frequently_terms],
				statuses: { ...state.statuses, frequentlyTerms: HttpStatus.FINISHED },
			}));
		} else {
			this.setState((state) => ({
				warnings: {
					...state.warnings,
					frequentlyTerms: body.warning.detail || body.warning.message,
				},
				statuses: { ...state.statuses, frequentlyTerms: HttpStatus.WARNING },
			}));
		}
	};

	uploadFilters = async () => {
		this.setState((state) => ({
			statuses: { ...state.statuses, filter: HttpStatus.LOADING },
		}));

		let filters: FilterFieldBase[];

		try {
			filters = await AnalysisAndTrainingApi.getFilter();
		} catch (e) {
			this.setState((state) => ({
				statuses: { ...state.statuses, filter: HttpStatus.FAILED },
			}));
			return;
		}

		this.setState((state) => ({
			filters: [...filters],
			statuses: { ...state.statuses, filter: HttpStatus.FINISHED },
		}));
	};

	applyFilters = async (filters: FilterFieldBase[]) => {
		this.setState((state) => ({
			filters: [],
			statuses: { ...state.statuses, filter: HttpStatus.LOADING },
		}));

		let response: { filters: FilterFieldBase[]; records_count: MainStatisticData | undefined };

		try {
			response = await AnalysisAndTrainingApi.saveFilter({
				action: "apply",
				filters: [
					...filters.filter((field) =>
						checkFieldIsFilled(field.filtration_type, field.current_value)
					),
				],
			});
		} catch (e) {
			this.setState((state) => ({
				filters,
				statuses: { ...state.statuses, filter: HttpStatus.FAILED },
			}));
			return;
		}

		if (response.records_count && response.records_count.filtered) {
			this.setState((state) => ({
				filters: response.filters,
				totalStatistic: response.records_count,
				statuses: { ...state.statuses, filter: HttpStatus.FINISHED },
			}));

			this.uploadDashboardData();
		} else {
			this.props.addToast(FiltersPopUp.noDataFound, ToastStyle.Warning);

			this.setState((state) => ({
				filters: response.filters,
				statuses: { ...state.statuses, filter: HttpStatus.FINISHED },
			}));
		}
	};

	resetFilters = async () => {
		this.setState((state) => ({
			filters: [],
			statuses: { ...state.statuses, filter: HttpStatus.LOADING },
		}));

		let response: { filters: FilterFieldBase[]; records_count: MainStatisticData | undefined };

		try {
			response = await AnalysisAndTrainingApi.saveFilter({
				action: "apply",
				filters: [],
			});
		} catch (e) {
			this.setState((state) => ({
				statuses: { ...state.statuses, filter: HttpStatus.FAILED },
			}));
			return;
		}

		this.setState((state) => ({
			filters: response.filters,
			totalStatistic: response.records_count,
			statuses: { ...state.statuses, filter: HttpStatus.FINISHED },
		}));

		this.uploadDashboardData();
	};

	uploadStatistic = async () => {
		this.setState((state) => ({
			statuses: { ...state.statuses, statistic: HttpStatus.LOADING },
		}));

		let statistic: AnalysisAndTrainingStatistic | undefined;

		try {
			statistic = await AnalysisAndTrainingApi.getStatistic();
		} catch (e) {
			this.setState((state) => ({
				statuses: { ...state.statuses, statistic: HttpStatus.FAILED },
			}));
			return;
		}

		if (this.validateUploadData(statistic, "statistic")) return;

		this.setState((state) => ({
			statistic,
			statuses: { ...state.statuses, statistic: HttpStatus.FINISHED },
		}));
	};

	uploadTotalStatistic = async () => {
		const { props } = this;

		this.setState({
			statuses: {
				filter: HttpStatus.LOADING,
				frequentlyTerms: HttpStatus.LOADING,
				defectSubmission: HttpStatus.LOADING,
				statistic: HttpStatus.LOADING,
				significantTerms: HttpStatus.LOADING,
			},
		});

		const totalStatistic = await AnalysisAndTrainingApi.getTotalStatistic();

		// check that data is collected
		if (totalStatistic.records_count) {
			// there is data
			this.setState({
				totalStatistic: { ...totalStatistic.records_count },
			});

			if (!totalStatistic.records_count.filtered) {
				props.addToast(
					"With cached filters we didn't find data. Try to change filter.",
					ToastStyle.Warning
				);

				this.setState((state) => ({
					isCollectingFinished: true,
					statuses: {
						...state.statuses,
						frequentlyTerms: HttpStatus.PREVIEW,
						defectSubmission: HttpStatus.PREVIEW,
						statistic: HttpStatus.PREVIEW,
						significantTerms: HttpStatus.PREVIEW,
					},
				}));
				props.setCollectingDataStatus(true);
			}
		} else {
			// there isn't data
			this.setState({
				isCollectingFinished: false,
				statuses: {
					filter: HttpStatus.PREVIEW,
					frequentlyTerms: HttpStatus.PREVIEW,
					defectSubmission: HttpStatus.PREVIEW,
					statistic: HttpStatus.PREVIEW,
					significantTerms: HttpStatus.PREVIEW,
				},
			});
			props.setCollectingDataStatus(false);
		}

		return totalStatistic.records_count ? totalStatistic.records_count.filtered : 0;
	};

	render() {
		const { state } = this;

		const blurIntensive = 10 - (state.loadingStatus / 100) * 9;
		const style = state.isCollectingFinished ? {} : { filter: `blur(${blurIntensive}px)` };

		return (
			<div className="at-page">
				<Header pageTitle="Analysis & Training">
					<div className="at-page__header-container">
					<MainStatistic className="at-page__main-statistic" statistic={state.totalStatistic} />

					<TrainingButton className="at-page__train-button" dashboardStatus={HttpStatus.FINISHED} />
					</div>
				</Header>

				{!state.isCollectingFinished && (
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
							status={state.statuses.filter}
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

								{state.filters.length && (
									<Filters
										className="configuration-tab__filters"
										filters={state.filters}
										applyFilters={this.applyFilters}
										resetFilters={this.resetFilters}
									/>
								)}
							</div>
						</Card>

						<Card
							previewImage={statisticsLoadingPreview}
							title="Statistics"
							status={state.statuses.statistic}
							className="statistics at-page__card"
							hoverHeader
						>
							{state.statistic && <Statistic statistic={state.statistic} />}
						</Card>
					</div>

					<div className="at-page__column at-page__column_position_right" style={style}>
						<Card
							previewImage={defectSubmissionLoadingPreview}
							title="Defect Submission"
							status={state.statuses.defectSubmission}
							className="defect-submission-card at-page__card"
						>
							<DefectSubmission
								defectSubmission={state.defectSubmission.data}
								activeTimeFilter={state.defectSubmission.activePeriod!}
								onChangePeriod={this.uploadDefectSubmission}
							/>
						</Card>

						<Card
							previewImage={frequentlyUsedTermsLoadingPreview}
							title="Frequently Used Terms"
							// status={HttpStatus.WARNING}
							status={state.statuses.frequentlyTerms}
							className="frequently-used-terms at-page__card"
							warningMessage={state.warnings.frequentlyTerms}
						>
							<FrequentlyUsedTerms frequentlyTermsList={state.frequentlyTerms} />
						</Card>

						<Card
							previewImage={significantTermsLoadingPreview}
							title="Significant Terms"
							status={state.statuses.significantTerms}
							className="at-page__significant-terms at-page__card"
							hoverHeader
						>
							<SignificantTerms
								status={state.statuses.significantTerms}
								onChangeMetric={this.uploadSignificantTermsList}
								metrics={state.significantTerms.metrics}
								chosen_metric={state.significantTerms.chosen_metric}
								terms={state.significantTerms.terms}
							/>
						</Card>
					</div>
				</div>
			</div>
		);
	}
}

const mapStateToProps = () => ({});

const mapDispatchToProps = {
	addToastWithAction,
	addToast,
	setCollectingDataStatus,
	removeToastByOuterId,
};

const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

export default connector(AnalysisAndTrainingPage);
