import { AnalysisAndTrainingApi } from 'app/common/api/analysis-and-training.api';
import Button, { ButtonStyled } from 'app/common/components/button/button';
import Card from 'app/common/components/card/card';
import { IconType } from 'app/common/components/icon/icon';
import { Timer } from 'app/common/functions/timer';
import { setCollectingDataStatus } from 'app/common/store/settings/actions';
import {
	AnalysisAndTrainingDefectSubmission,
	AnalysisAndTrainingStatistic,
} from 'app/common/types/analysis-and-training.types';
import { HttpStatus } from 'app/common/types/http.types';
import DefectSubmission from 'app/modules/defect-submission/defect-submission';
import { FilterFieldBase } from 'app/modules/filters/field/field-type';
import { checkFieldIsFilled } from 'app/modules/filters/field/field.helper-function';
import { Filters } from 'app/modules/filters/filters';
import FrequentlyUsedTerms from 'app/modules/frequently-used-terms/frequently-used-terms';
import Header from 'app/modules/header/header';
import MainStatistic, { MainStatisticData } from 'app/modules/main-statistic/main-statistic';
import SignificantTerms from 'app/modules/significant-terms/significant-terms';
import { Terms } from 'app/modules/significant-terms/store/types';
import Statistic from 'app/modules/statistic/statistic';
import { addToast, addToastWithAction } from 'app/modules/toasts-overlay/store/actions';
import { ToastStyle } from 'app/modules/toasts-overlay/store/types';
import TrainingButton from 'app/modules/training-button/training-button';

import 'app/pages/analysis-and-training/analysis-and-training.page.scss';

import calculateData1 from 'assets/images/calculateData1.svg';
import calculateData2 from 'assets/images/calculateData2.svg';
import calculateData3 from 'assets/images/calculateData3.svg';

import defectSubmissionLoadingPreview from 'assets/images/defect-submission-loading-preview.png';
import filterLoadingPreview from 'assets/images/filter-loading-preview.png';
import frequentlyUsedTermsLoadingPreview from 'assets/images/frequently-used-terms-loading-preview.png';
import significantTermsLoadingPreview from 'assets/images/significant-terms-loading-preview.png';
import statisticsLoadingPreview from 'assets/images/statistics-loading-preview.png';
import { socket } from 'index';
import React from 'react';
import { connect, ConnectedProps } from 'react-redux';
import { removeToastByOuterId } from "app/modules/toasts-overlay/store/actions";

interface State {
	loadingStatus: number,
	filters: FilterFieldBase[],
	totalStatistic: MainStatisticData | undefined,
	frequentlyTerms: string[],
	isCollectingFinished: boolean,
	statistic: AnalysisAndTrainingStatistic | undefined,
	significantTerms: {
		metrics: string[],
		chosen_metric: string | null,
		terms: Terms
	},
	defectSubmission: {
		data: AnalysisAndTrainingDefectSubmission | undefined,
		activePeriod: string | undefined,
	},
	statuses: {
		[key: string]: HttpStatus,
		filter: HttpStatus,
		frequentlyTerms: HttpStatus,
		defectSubmission: HttpStatus,
		statistic: HttpStatus,
		significantTerms: HttpStatus
	},
	warnings: {
		frequentlyTerms: string
	}
}

const LOADING_TIME = 5 * 60 * 1000;

class AnalysisAndTrainingPage extends React.Component<PropsFromRedux, State> {

	interval: NodeJS.Timer | null = null;
	timer: Timer | null = null;
	isComponentMounted: boolean = false;
	updateDataToastID: number = 0;

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
			frequentlyTerms: '',
		},
	};

	constructor(props: PropsFromRedux) {
		super(props);
		this.props.setCollectingDataStatus(this.state.isCollectingFinished);

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

	uploadDashboardData = (typeUpload: 'full' | 'data' | 'filters' = 'data') => {
		if (typeUpload === 'full' || typeUpload === 'filters') {
			this.uploadFilters();
		}

		if (typeUpload === 'full' || typeUpload === 'data') {
			this.uploadFrequentlyTerms();
			this.uploadStatistic();
			this.uploadDefectSubmission();
			this.uploadSignificantTermsData();
		}
	};

	componentDidMount(): void {
		this.isComponentMounted = true;
		this.uploadTotalStatistic()
			.then(() => {
				if (this.state.isCollectingFinished) {
					if (this.state.totalStatistic?.filtered) {
						this.uploadDashboardData('full');
					} else {
						this.uploadDashboardData('filters');
					}
				}
			});

		this.startSocket();
	}

	componentWillUnmount = () => {  
		this.isComponentMounted = false;
		if(this.updateDataToastID) {
			this.props.removeToastByOuterId(this.updateDataToastID);
		} 
	}

	startSocket = () => {
		socket.startMonitor('message', (val) => {
			if (this.state.isCollectingFinished && this.isComponentMounted) {  
				++this.updateDataToastID;
				this.props.addToastWithAction('Data has been updated', ToastStyle.Info, [
					{
						buttonName: 'Load',
						callBack: () => {
							this.uploadTotalStatistic().then(_=> this.uploadDashboardData('full'));
						},
					},
				], this.updateDataToastID);
				
			} else if(!this.state.isCollectingFinished){
				document.location.reload();
			}
		});
	};

	componentDidUpdate(prevProps: Readonly<PropsFromRedux>, prevState: Readonly<State>, snapshot?: any): void {
		if (!this.state.isCollectingFinished && !this.interval) {
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

	validateUploadData = (data: any, cardName: string) => {
		if(!(data && Object.keys(data).length)){
			this.setState({
				statuses: {...this.state.statuses, [cardName]: HttpStatus.PREVIEW}
			});
			return true;
		}
		return false;
	}

	uploadSignificantTermsData = async () => {
		this.setState({
			statuses: { ...this.state.statuses, significantTerms: HttpStatus.LOADING },
		});

		try {
			let { significant_terms } = await AnalysisAndTrainingApi.getSignificantTermsData();

			if(this.validateUploadData(significant_terms, "significantTerms")) return; 

			this.setState({
				statuses: { ...this.state.statuses, significantTerms: HttpStatus.FINISHED },
				significantTerms: {
					metrics: [...significant_terms.metrics],
					chosen_metric: significant_terms.chosen_metric,
					terms: { ...significant_terms.terms },
				},
			});
		} catch (e) {
			this.setState({
				statuses: { ...this.state.statuses, significantTerms: HttpStatus.FAILED },
			});
		}
	};

	uploadSignificantTermsList = async (metric: string) => {
		this.setState({
			statuses: { ...this.state.statuses, significantTerms: HttpStatus.LOADING },
			significantTerms: {
				...this.state.significantTerms,
				chosen_metric: metric,
			},
		});

		try {
			let { significant_terms } = await AnalysisAndTrainingApi.getSignificantTermsList(metric);

			if(this.validateUploadData(significant_terms, "significantTerms")) return;

			this.setState({
				statuses: { ...this.state.statuses, significantTerms: HttpStatus.FINISHED },
				significantTerms: {
					...this.state.significantTerms,
					terms: { ...significant_terms },
				},
			});
		} catch (e) {
			this.setState({
				statuses: { ...this.state.statuses, significantTerms: HttpStatus.FAILED },
			});
		}
	};

	uploadDefectSubmission = async (period?: string) => {
		this.setState({
			defectSubmission: {
				...this.state.defectSubmission,
				activePeriod: period,
			},
			statuses: { ...this.state.statuses, defectSubmission: HttpStatus.LOADING },
		});

		try {
			let defectSubmission = await AnalysisAndTrainingApi.getDefectSubmission(period);

			if(this.validateUploadData(defectSubmission, "defectSubmission")) return;

			this.setState({
				defectSubmission: {
					data: defectSubmission.defect_submission,
					activePeriod: defectSubmission.period,
				},
				statuses: { ...this.state.statuses, defectSubmission: HttpStatus.FINISHED },
			});
		} catch (e) {
			this.setState({
				statuses: { ...this.state.statuses, defectSubmission: HttpStatus.FAILED },
			});
		}
	};

	uploadFrequentlyTerms = async () => {
		this.setState({
			statuses: { ...this.state.statuses, frequentlyTerms: HttpStatus.LOADING },
		});

		try {
			let body: any = await AnalysisAndTrainingApi.getFrequentlyTerms();

			if(this.validateUploadData(body, "frequentlyTerms")) return;

			if (body.frequently_terms) {
				this.setState({
					frequentlyTerms: [...body.frequently_terms],
					statuses: { ...this.state.statuses, frequentlyTerms: HttpStatus.FINISHED },
				});
			} else {
				this.setState({
					warnings: {
						...this.state.warnings,
						frequentlyTerms: body.warning.detail || body.warning.message,
					},
					statuses: { ...this.state.statuses, frequentlyTerms: HttpStatus.WARNING },
				});
			}
		} catch (e) {
			this.setState({
				statuses: { ...this.state.statuses, frequentlyTerms: HttpStatus.FAILED },
			});
		}
	};

	uploadFilters = async () => {
		this.setState({
			statuses: { ...this.state.statuses, filter: HttpStatus.LOADING },
		});

		try {
			let filters = await AnalysisAndTrainingApi.getFilter();

			this.setState({
				filters: [...filters],
				statuses: { ...this.state.statuses, filter: HttpStatus.FINISHED },
			});
		} catch (e) {
			this.setState({
				statuses: { ...this.state.statuses, filter: HttpStatus.FAILED },
			});
		}
	};

	applyFilters = async (filters: FilterFieldBase[]) => {
		this.setState({
			filters: [],
			statuses: { ...this.state.statuses, filter: HttpStatus.LOADING },
		});

		try {
			let response = await AnalysisAndTrainingApi.saveFilter({
				action: 'apply',
				filters: [...filters.filter((field) => checkFieldIsFilled(field.filtration_type, field.current_value))],
			});

			if (response.records_count.filtered) {
				this.setState({
					filters: response.filters,
					totalStatistic: response.records_count,
					statuses: { ...this.state.statuses, filter: HttpStatus.FINISHED },
				});

				this.uploadDashboardData();
			} else {
				this.props.addToast('Data cannot be found. Please change filters.', ToastStyle.Warning);

				this.setState({
					filters: response.filters,
					statuses: { ...this.state.statuses, filter: HttpStatus.FINISHED },
				});
			}

		} catch (e) {
			this.setState({
				filters,
				statuses: { ...this.state.statuses, filter: HttpStatus.FAILED },
			});
		}
	};

	resetFilters = async () => {
		this.setState({
			filters: [],
			statuses: { ...this.state.statuses, filter: HttpStatus.LOADING },
		});

		try {
			let response = await AnalysisAndTrainingApi.saveFilter({
				action: 'apply',
				filters: [],
			});

			this.setState({
				filters: response.filters,
				totalStatistic: response.records_count,
				statuses: { ...this.state.statuses, filter: HttpStatus.FINISHED },
			});

			this.uploadDashboardData();
		} catch (e) {
			this.setState({
				statuses: { ...this.state.statuses, filter: HttpStatus.FAILED },
			});
		}
	};

	uploadStatistic = async () => {
		this.setState({
			statuses: { ...this.state.statuses, statistic: HttpStatus.LOADING },
		});

		try {
			let statistic = await AnalysisAndTrainingApi.getStatistic();

			if(this.validateUploadData(statistic, "statistic")) return;

			this.setState({
				statistic,
				statuses: { ...this.state.statuses, statistic: HttpStatus.FINISHED },
			});
		} catch (e) {
			this.setState({
				statuses: { ...this.state.statuses, statistic: HttpStatus.FAILED },
			});
		}
	};

	uploadTotalStatistic = async () => {
		this.setState({
			statuses: {
				filter: HttpStatus.LOADING,
				frequentlyTerms: HttpStatus.LOADING,
				defectSubmission: HttpStatus.LOADING,
				statistic: HttpStatus.LOADING,
				significantTerms: HttpStatus.LOADING,
			},
		});

		let totalStatistic = await AnalysisAndTrainingApi.getTotalStatistic();

		// check that data is collected
		if (totalStatistic.records_count) {
			// there is data
			this.setState({
				totalStatistic: { ...totalStatistic.records_count },
			});

			if (!totalStatistic.records_count.filtered) {
				this.props.addToast('With cached filters we didn\'t find data. Try to change filter.', ToastStyle.Warning);

				this.setState({
					isCollectingFinished: true,
					statuses: {
						...this.state.statuses,
						frequentlyTerms: HttpStatus.PREVIEW,
						defectSubmission: HttpStatus.PREVIEW,
						statistic: HttpStatus.PREVIEW,
						significantTerms: HttpStatus.PREVIEW,
					},
				});
				this.props.setCollectingDataStatus(true);
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
			this.props.setCollectingDataStatus(false);
		}
	};

	render() {
		let blurIntensive = 10 - (this.state.loadingStatus / 100 * 9);
		let style = this.state.isCollectingFinished ? {} : { filter: `blur(${blurIntensive}px)` };

		return (
			<div className="at-page">
				<Header pageTitle="Analysis & Training">
					<MainStatistic className="at-page__main-statistic" statistic={this.state.totalStatistic} />

					<TrainingButton className="at-page__train-button" dashboardStatus={HttpStatus.FINISHED} />
				</Header>

				{
					!this.state.isCollectingFinished &&
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
							className="configuration-tab at-page__card at-page__card_filter"
							previewImage={filterLoadingPreview}
							status={this.state.statuses.filter}
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
							status={this.state.statuses.statistic}
							className="statistics at-page__card"
							hoverHeader
						>
							{this.state.statistic && <Statistic statistic={this.state.statistic} />}
						</Card>

					</div>

					<div className="at-page__column at-page__column_position_right" style={style}>
						<Card
							previewImage={defectSubmissionLoadingPreview} title="Defect Submission"
							status={this.state.statuses.defectSubmission}
							className="defect-submission-card at-page__card"
						>
							<DefectSubmission
								defectSubmission={this.state.defectSubmission.data}
								activeTimeFilter={this.state.defectSubmission.activePeriod!}
								onChangePeriod={this.uploadDefectSubmission}
							/>
						</Card>

						<Card
							previewImage={frequentlyUsedTermsLoadingPreview} title="Frequently Used Terms"
							// status={HttpStatus.WARNING}
							status={this.state.statuses.frequentlyTerms}
							className="frequently-used-terms at-page__card"
							warningMessage={this.state.warnings.frequentlyTerms}
						>
							<FrequentlyUsedTerms frequentlyTermsList={this.state.frequentlyTerms} />
						</Card>

						<Card
							previewImage={significantTermsLoadingPreview} title="Significant Terms"
							status={this.state.statuses.significantTerms}
							className="at-page__significant-terms at-page__card" hoverHeader
						>
							<SignificantTerms
								status={this.state.statuses.significantTerms}
								onChangeMetric={this.uploadSignificantTermsList}
								metrics={this.state.significantTerms.metrics}
								chosen_metric={this.state.significantTerms.chosen_metric}
								terms={this.state.significantTerms.terms}
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
	removeToastByOuterId
};

const connector = connect(
	mapStateToProps,
	mapDispatchToProps,
);

type PropsFromRedux = ConnectedProps<typeof connector>

export default connector(AnalysisAndTrainingPage);
