import Card from "app/common/components/card/card";
import { CustomBarChart } from "app/common/components/charts/bar-chart/bar-chart";
import DonutChart, {
	DonutChartColorSchemes,
} from "app/common/components/charts/donut-chart/donut-chart";
import { TagCloud } from "app/common/components/charts/tag-cloud/tag-cloud";
import DropdownElement
	from "app/common/components/native-components/dropdown-element/dropdown-element";
import { DAPrioritySortBy } from "app/common/store/description-assessment/types";
import { connect, ConnectedProps } from "react-redux";

import Header from "app/modules/header/header";

import PredictText from "app/modules/predict-text/predict-text";

import bugResolutionPreview from "assets/images/dAssessment__bug-resolution__preview.png";
import priorityPreview from "assets/images/dAssessment__priority__preview.png";
import testingProbabilityPreview from "assets/images/dAssessment__testing-probability__preview.png";
import textFieldPreview from "assets/images/dAssessment__text-field__preview.png";
import ttrPreview from "assets/images/dAssessment__ttr__preview.png";
import notTrainModel1 from "assets/images/notTrainModel1.svg";
import notTrainModel2 from "assets/images/notTrainModel2.svg";
import notTrainModel3 from "assets/images/notTrainModel3.svg";
import React from "react";

import "./description-assessment.page.scss";
import {
	getMetrics,
	predictText,
	getKeywords,
} from "app/common/store/description-assessment/thunk";
import {
	sortDAPriority,
	clearPageData
} from "app/common/store/description-assessment/actions";
import { RootStore } from "app/common/types/store.types";
import { HttpStatus } from "app/common/types/http.types";

class DescriptionAssessmentPage extends React.Component<PropsFromRedux> {
	imageForNotTrainingModel = "";

	constructor(props: PropsFromRedux) {
		super(props);

		this.randomImageForNotTrainingModel();
	}

	componentDidMount() {
		if (this.props.isModelFounded) {
			this.props.getMetrics(true);
		}
	}

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

	sortPriority = (newValue: string) => {
		this.props.sortDAPriority(newValue as DAPrioritySortBy);
	}

	render() {
		const showPreview = this.props.isSearchingModelFinished && !this.props.isModelFounded;
		const style = showPreview ? { filter: `blur(3px)` } : {};

		const predictTextStatus = showPreview ? this.props.status : HttpStatus.FINISHED;

		return (
			<div className="dAssessment-page">
				<Header pageTitle="Description Assessment" />

				{showPreview && (
					<div className="dAssessment-page__collecting-data collecting-data">
						<div className="collecting-data__message">
							Can't calculate predictions. Please train models.
						</div>

						<img src={this.imageForNotTrainingModel} alt="Can't calculate predictions" />
					</div>
				)}

				<div className="dAssessment-page__content">
					<div
						className="dAssessment-page__column dAssessment-page__column_position_left"
						style={style}
					>
						<Card
							previewImage={textFieldPreview}
							status={predictTextStatus}
							className="text-field dAssessment-page__card"
						>
							<PredictText
								availableMetricsValues={this.props.metrics}
								onPredict={this.props.predictText}
								onClearAll={this.props.clearPageData}
								onChangePredictOption={this.props.getKeywords}
								keywords={this.props.keywords}
								text={this.props.text}
							/>
						</Card>

						<Card
							previewImage={testingProbabilityPreview}
							title="Area Of Testing Probability"
							status={this.props.status}
							className="probability dAssessment-page__card"
						>
							{this.props.probabilities && (
								<TagCloud tags={this.props.probabilities.areas_of_testing} percentage />
							)}
						</Card>
					</div>

					<div
						className="dAssessment-page__column dAssessment-page__column_position_right"
						style={style}
					>
						<Card
							previewImage={bugResolutionPreview}
							title="Bug Resolution"
							status={this.props.status}
							className="bug-resolution dAssessment-page__card"
							hoverHeader
						>
							{this.props.probabilities && (
								<div className="bug-resolution__charts">
									{this.props.probabilities.resolution.map((chart, index) => (
										<DonutChart
											key={index}
											className="bug-resolution__chart"
											data={chart.data}
											colorSchema={
												index % 2 === 0
													? DonutChartColorSchemes.greenBlue
													: DonutChartColorSchemes.orangeViolet
											}
										/>
									))}
								</div>
							)}
						</Card>

						<Card
							previewImage={priorityPreview}
							title="Priority"
							status={this.props.status}
							className="priority dAssessment-page__card"
						>
							{this.props.probabilities && (
								<>
									<div className="priority__select-wrapper">
										<div className="priority__select-wrapper-label">
											Sort by
										</div>
										<DropdownElement
											writable={false}
											dropDownValues={[
												{ value: DAPrioritySortBy.Value, label: 'Priority'},
												{ value: DAPrioritySortBy.Name, label: 'Name'},
											]}
											value={
												{ value: DAPrioritySortBy.Value, label: 'Priority'}
											}
											onChange={this.sortPriority}
											className="priority__dropdown"
										/>
									</div>


									<CustomBarChart percentage data={this.props.probabilities.Priority} />
								</>
							)}
						</Card>

						<Card
							previewImage={ttrPreview}
							title="Time to Resolve (TTR)"
							status={this.props.status}
							className="ttr dAssessment-page__card"
						>
							{this.props.probabilities && (
								<CustomBarChart
									data={this.props.probabilities["Time to Resolve"]}
									verticalDirection
									multiColors
									percentage
								/>
							)}
						</Card>
					</div>
				</div>
			</div>
		);
	}
}

const mapStateToProps = ({ descriptionAssessment, common }: RootStore) => ({
	...descriptionAssessment,
	isModelFounded: common.isModelFounded,
	isSearchingModelFinished: common.isSearchingModelFinished,
});

const mapDispatchToProps = {
	getMetrics,
	predictText,
	getKeywords,
	clearPageData,
	sortDAPriority
};

const connector = connect(mapStateToProps, mapDispatchToProps);
type PropsFromRedux = ConnectedProps<typeof connector>;

export default connector(DescriptionAssessmentPage);
