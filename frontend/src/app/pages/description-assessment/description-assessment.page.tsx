import { DescriptionAssessmentApi } from 'app/common/api/description-assessment.api';

import Card from 'app/common/components/card/card';
import { CustomBarChart } from 'app/common/components/charts/bar-chart/bar-chart';
import DonutChart, {
	DonutChartColorSchemes,
	DonutChartData,
} from 'app/common/components/charts/donut-chart/donut-chart';
import { TagCloud } from 'app/common/components/charts/tag-cloud/tag-cloud';
import { HttpStatus } from 'app/common/types/http.types';
import { connect, ConnectedProps } from 'react-redux';

import Header from 'app/modules/header/header';

import PredictText, { PredictMetric, Keywords } from 'app/modules/predict-text/predict-text';
import { Terms } from 'app/modules/significant-terms/store/types';

import bugResolutionPreview from 'assets/images/dAssessment__bug-resolution__preview.png';
import priorityPreview from 'assets/images/dAssessment__priority__preview.png';
import testingProbabilityPreview from 'assets/images/dAssessment__testing-probability__preview.png';
import textFieldPreview from 'assets/images/dAssessment__text-field__preview.png';
import ttrPreview from 'assets/images/dAssessment__ttr__preview.png';
import notTrainModel1 from 'assets/images/notTrainModel1.svg';
import notTrainModel2 from 'assets/images/notTrainModel2.svg';
import notTrainModel3 from 'assets/images/notTrainModel3.svg';
import React from 'react';

import './description-assessment.page.scss';
import { addToast } from 'app/modules/toasts-overlay/store/actions';
import { ToastStyle } from 'app/modules/toasts-overlay/store/types';
import { fixTTRBarChartAxisDisplayStyle } from 'app/common/functions/helper';

export interface DAProbabilitiesData {
	[key: string]: unknown
}

export interface DAProbabilitiesResolutionChartData {
	[key: string]: DAProbabilitiesData
}

interface Probabilities {
	resolution: DAProbabilitiesResolutionChartData,
	areas_of_testing: DAProbabilitiesData,
	'Time to Resolve': DAProbabilitiesData,
	Priority: DAProbabilitiesData,
}

interface State {
	status: HttpStatus,
	isModelTrained: boolean,
	metrics: Keywords,
	keywords: Keywords
	probabilities: Probabilities | null,
}

class DescriptionAssessmentPage extends React.Component<PropsFromRedux, State> {

	state = {
		status: HttpStatus.PREVIEW,
		isModelTrained: true,
		metrics: emptyMetrics,
		keywords: emptyMetrics,
		probabilities: null,
	};

	imageForNotTrainingModel: string = '';

	randomImageForNotTrainingModel = () => {
		switch (Math.floor(Math.random() * 3)) {
			case 1:
				this.imageForNotTrainingModel = notTrainModel1;
				break;
			case 2:
				this.imageForNotTrainingModel = notTrainModel2;
				break;
			default:
				this.imageForNotTrainingModel = notTrainModel3;
				break;
		}
	};

	componentDidMount() {
		this.randomImageForNotTrainingModel();

		this.getMetrics(true);
	}

	predictText = (text: string) => {
		this.setState({ status: HttpStatus.LOADING });

		DescriptionAssessmentApi.predictText(text)
			.then((data) => { 
				if(data.warning) throw new Error(data.warning.detail || data.warning.message);
				let {probabilities} = data;
				
				this.setState({
					status: HttpStatus.FINISHED,
					probabilities: {
						resolution: { ...probabilities.resolution },
						areas_of_testing: { ...probabilities.areas_of_testing },
						'Time to Resolve': { ...fixTTRBarChartAxisDisplayStyle(probabilities['Time to Resolve'])},
						Priority: { ...probabilities.Priority },
					},
				});
				this.getMetrics();
			})
			.catch(err =>{ 
				this.props.addToast(err.message, ToastStyle.Error);
				this.setState({ status: HttpStatus.FAILED });
			});
	};

	clearAll = () => {
		this.setState({
			status: HttpStatus.PREVIEW,
			metrics: emptyMetrics,
			keywords: emptyMetrics,
			probabilities: null,
		});
	};

	getKeywords = async (predictMetric: PredictMetric) => {
		let newKeywords: string[];

		// for reset keywords
		if (predictMetric.value) {
			newKeywords = (await DescriptionAssessmentApi.getHighlightedTerms(predictMetric)).terms;
		} else {
			newKeywords = [];
		}

		this.setState((state)=>({
			keywords: {
				...state.keywords,
				[predictMetric.metric]: newKeywords,
			},
		}));
	};

	getMetrics = (empty: boolean = false) => {
		DescriptionAssessmentApi.getMetrics()
			.then((metrics) => {
				if (metrics.warning) {
					this.setState({ isModelTrained: false });
					this.props.addToast(metrics.warning.detail, ToastStyle.Warning);
					return;
				}
				if (!empty) {
					this.setState({ metrics });
				}
			})
			.catch(() => this.setState({ isModelTrained: false }));
	};

	render() {
		let style = this.state.isModelTrained ? {} : { filter: `blur(3px)` };
		return (
			<div className="dAssessment-page">
				<Header pageTitle="Description Assessment" />

				{
					!this.state.isModelTrained &&
          <div className="dAssessment-page__collecting-data collecting-data">
              <div className="collecting-data__message">
                  Can't calculate predictions. Please train models.
              </div>

              <img src={this.imageForNotTrainingModel} alt="Can't calculate predictions" />
          </div>
				}

				<div className="dAssessment-page__content">
					<div className="dAssessment-page__column dAssessment-page__column_position_left" style={style}>
						<Card
							previewImage={textFieldPreview}
							status={HttpStatus.FINISHED}
							className="text-field dAssessment-page__card"
						>
							<PredictText
								availableMetricsValues={this.state.metrics}
								onPredict={this.predictText}
								onClearAll={this.clearAll}
								onChangePredictOption={this.getKeywords}
								keywords={this.state.keywords}
							/>
						</Card>

						<Card
							previewImage={testingProbabilityPreview} title="Area Of Testing Probability"
							status={this.state.status}
							className="probability dAssessment-page__card"
						>
							{
								this.state.probabilities &&
                <TagCloud
		                tags={(this.state.probabilities! as Probabilities).areas_of_testing as Terms}
                    percentage
                />
							}
						</Card>

					</div>

					<div className="dAssessment-page__column dAssessment-page__column_position_right" style={style}>
						<Card
							previewImage={bugResolutionPreview} title="Bug Resolution"
							status={this.state.status}
							className="bug-resolution dAssessment-page__card"
							hoverHeader
						>
							{
								this.state.probabilities &&
                <div className="bug-resolution__charts">
									{
										Object.values((this.state.probabilities! as Probabilities).resolution).map((data, index) => (
											<DonutChart
												key={index}
												className="bug-resolution__chart"
												data={data as DonutChartData}
												colorSchema={index % 2 === 0 ? DonutChartColorSchemes.greenBlue : DonutChartColorSchemes.orangeViolet}
											/>
										))
									}
                </div>
							}
						</Card>

						<Card
							previewImage={priorityPreview} title="Priority"
							status={this.state.status}
							className="priority dAssessment-page__card"
						>
							{
								this.state.probabilities &&
                <CustomBarChart
                    percentage={true}
                    data={(this.state.probabilities! as Probabilities).Priority as DonutChartData}
                />
							}
						</Card>

						<Card
							previewImage={ttrPreview} title="Time to Resolve (TTR)"
							status={this.state.status}
							className="ttr dAssessment-page__card"
						>
							{
								this.state.probabilities &&
                <CustomBarChart
                    data={(this.state.probabilities! as Probabilities)['Time to Resolve'] as DonutChartData}
                    verticalDirection
                    multiColors
                    percentage
                />
							}
						</Card>
					</div>
				</div>
			</div>
		);
	}
}

const mapDispatchToProps = {
	addToast,
};

const connector = connect(
	undefined,
	mapDispatchToProps,
);
type PropsFromRedux = ConnectedProps<typeof connector>;

export default connector(DescriptionAssessmentPage);

const emptyMetrics = {
	Priority: [],
	resolution: [],
	areas_of_testing: [],
};
