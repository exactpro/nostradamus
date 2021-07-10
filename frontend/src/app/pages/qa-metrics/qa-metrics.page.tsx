import Button, { ButtonStyled } from "app/common/components/button/button";

import Card from "app/common/components/card/card";
import { CustomBarChart } from "app/common/components/charts/bar-chart/bar-chart";
import DonutChart, {
	DonutChartColorSchemes,
} from "app/common/components/charts/donut-chart/donut-chart";
import { TagCloud } from "app/common/components/charts/tag-cloud/tag-cloud";
import CircleSpinner from "app/common/components/circle-spinner/circle-spinner";
import { IconType } from "app/common/components/icon/icon";
import DropdownElement
	from "app/common/components/native-components/dropdown-element/dropdown-element";
import { changeQAMetricsPrioritySortBy } from "app/common/store/qa-metrics/actions";
import {
	applyQAMetricsFilters,
	getQAMetricsData,
	updateQAMetricsData,
	updateQAMetricsTable,
} from "app/common/store/qa-metrics/thunks";
import { QAMetricsPrioritySortBy } from "app/common/store/qa-metrics/types";
import { HttpStatus } from "app/common/types/http.types";
import { RootStore } from "app/common/types/store.types";
import { FilterFieldBase } from "app/modules/filters/field/field-type";
import { Filters } from "app/modules/filters/filters";

import Header from "app/modules/header/header";
import MainStatistic from "app/modules/main-statistic/main-statistic";
import PredictionsTable from "app/modules/predictions-table/predictions-table";

import bugResolutionPreview from "assets/images/dAssessment__bug-resolution__preview.png";
import priorityPreview from "assets/images/dAssessment__priority__preview.png";
import testingProbabilityPreview from "assets/images/dAssessment__testing-probability__preview.png";
import ttrPreview from "assets/images/dAssessment__ttr__preview.png";
import filterLoadingPreview from "assets/images/filter-loading-preview.png";
import notTrainModel1 from "assets/images/notTrainModel1.svg";
import notTrainModel2 from "assets/images/notTrainModel2.svg";
import notTrainModel3 from "assets/images/notTrainModel3.svg";
import React from "react";
import { connect, ConnectedProps } from "react-redux";

import "./qa-metrics.page.scss";

class QAMetricsPage extends React.PureComponent<PropsFromRedux> {
	imageForNotTrainingModel = "";
	modelIsTraining = false;

	componentDidMount() {
		this.randomImageForNotTrainingModel();

		if (this.props.records_count.total === 0) {
			this.props.getQAMetricsData();
		}

		if (this.props.trainingStatus === HttpStatus.RELOADING) {
			this.modelIsTraining = true;
		}
	}

	componentDidUpdate() {
		if (this.modelIsTraining && this.props.trainingStatus === HttpStatus.FINISHED) {
			this.modelIsTraining = false;
			this.props.getQAMetricsData();
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

	loadNewTableData = (pageIndex: number, limit: number) => {
		this.props.updateQAMetricsTable(limit, (pageIndex - 1) * limit);
	};

	applyFilters = (filters: FilterFieldBase[]) => {
		this.props.applyQAMetricsFilters(filters);
	};

	resetFilters = () => {
		this.props.applyQAMetricsFilters([]);
	};

	changeSort = (newValue: string) => {
		this.props.changeQAMetricsPrioritySortBy(newValue as QAMetricsPrioritySortBy);
	}

	render() {
		const showPreview = this.props.isSearchingModelFinished && !this.props.isModelFounded;
		const style = showPreview ? { filter: `blur(3px)` } : {};

		return (
			<div className="qa-metrics-page">
				<Header pageTitle="QA Metrics">
					<MainStatistic
						className="qa-metrics-page__main-statistic"
						statistic={this.props.records_count}
					/>
				</Header>

				{showPreview && (
					<div className="qa-metrics-page__collecting-data collecting-data">
						<div className="collecting-data__message">
							{this.props.trainingStatus === HttpStatus.RELOADING
								? "Model is training. Please wait ..."
								: "Can't calculate predictions. Please train models."}
						</div>

						<img src={this.imageForNotTrainingModel} alt="Can't calculate predictions" />
					</div>
				)}

				<div className="qa-metrics-page__content">
					<div
						className="qa-metrics-page__column qa-metrics-page__column_position_left"
						style={style}
					>
						<Card
							previewImage={filterLoadingPreview}
							status={this.props.statuses.filter}
							className={`qa-metric-filters qa-metrics-page__card ${
								this.props.statuses.filter === HttpStatus.LOADING && "qa-metric-filters_shifted"
							}`}
						>
							<div className="qa-metric-filters__container">
								<Button
									className="qa-metric-filters__section-filters"
									text="Filter"
									icon={IconType.filter}
									styled={ButtonStyled.Flat}
									selected
								/>

								<Filters
									className="qa-metric-filters__filter"
									filters={this.props.filter}
									applyFilters={this.applyFilters}
									resetFilters={this.resetFilters}
								/>
							</div>
						</Card>

						<Card
							previewImage={testingProbabilityPreview}
							title="Area Of Testing Probability"
							status={this.props.statuses.data}
							className="probability qa-metrics-page__card"
						>
							<TagCloud tags={this.props.areas_of_testing_chart} percentage />
						</Card>
					</div>

					<div
						className="qa-metrics-page__column qa-metrics-page__column_position_right"
						style={style}
					>
						<Card
							previewImage={bugResolutionPreview}
							title="Bug Resolution"
							status={this.props.statuses.data}
							className="bug-resolution qa-metrics-page__card"
							hoverHeader
						>
							<div className="bug-resolution__charts">
								{this.props.resolution_chart.map((chart, index) => (
									// eslint-disable-next-line react/no-array-index-key
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
						</Card>

						<Card
							previewImage={priorityPreview}
							title="Priority"
							status={this.props.statuses.data}
							className="priority qa-metrics-page__card"
						>
							<div className="priority__select-wrapper">
								<div className="priority__select-wrapper-label">
									Sort by
								</div>
								<DropdownElement
									writable={false}
									dropDownValues={[
										{ value: QAMetricsPrioritySortBy.Value, label: 'Priority'},
										{ value: QAMetricsPrioritySortBy.Name, label: 'Name'},
									]}
									value={
										{ value: QAMetricsPrioritySortBy.Value, label: 'Priority'}
									}
									onChange={this.changeSort}
									className="priority__dropdown"
								/>
							</div>

							<CustomBarChart data={this.props.priority_chart} />
						</Card>

						<Card
							previewImage={ttrPreview}
							title="Time to Resolve (TTR)"
							status={this.props.statuses.data}
							className="ttr qa-metrics-page__card"
						>
							<CustomBarChart
								data={this.props.ttr_chart}
								verticalDirection
								multiColors
								percentage
							/>
						</Card>
					</div>
				</div>

				{this.props.statuses.data === HttpStatus.FINISHED && (
					<div className="qa-metrics-page__content" style={style}>
						<Card
							title="Predictions Table"
							className="qa-metrics-page__predictions-table qa-metrics-page__card"
							hoverHeader
						>
							{this.props.statuses.table === HttpStatus.RELOADING && <CircleSpinner alignCenter />}

							<PredictionsTable
								tableData={this.props.predictions_table}
								totalCount={this.props.prediction_table_rows_count}
								onChangePage={this.loadNewTableData}
							/>
						</Card>
					</div>
				)}
			</div>
		);
	}
}

const mapStateToProps = (state: RootStore) => ({
	isModelFounded: state.common.isModelFounded,
	isSearchingModelFinished: state.common.isSearchingModelFinished,
	trainingStatus: state.training.status,
	statuses: state.qaMetricsPage.statuses,
	filter: state.qaMetricsPage.filter,
	predictions_table: state.qaMetricsPage.predictions_table,
	prediction_table_rows_count: state.qaMetricsPage.prediction_table_rows_count,
	areas_of_testing_chart: state.qaMetricsPage.areas_of_testing_chart,
	priority_chart: state.qaMetricsPage.priority_chart,
	ttr_chart: state.qaMetricsPage.ttr_chart,
	resolution_chart: state.qaMetricsPage.resolution_chart,
	records_count: state.qaMetricsPage.records_count,
});

const mapDispatchToProps = {
	updateQAMetricsData,
	updateQAMetricsTable,
	applyQAMetricsFilters,
	getQAMetricsData,
	changeQAMetricsPrioritySortBy
};

const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;

export default connector(QAMetricsPage);
