import { CustomBarChart } from 'app/common/components/charts/bar-chart/bar-chart';
import DonutChart, {
	DonutChartColorSchemes,
	DonutChartData,
} from 'app/common/components/charts/donut-chart/donut-chart';
import { TagCloud } from 'app/common/components/charts/tag-cloud/tag-cloud';
import CircleSpinner from 'app/common/components/circle-spinner/circle-spinner';
import {
	updateQAMetricsData,
	updateQAMetricsFilters,
	updateQAMetricsTable,
} from 'app/common/store/qa-metrics/thunks';
import { RootStore } from 'app/common/types/store.types';
import { FilterFieldBase } from 'app/modules/filters/field/field-type';
import { Filters } from 'app/modules/filters/filters';
import PredictionsTable from 'app/modules/predictions-table/predictions-table';
import { Terms } from 'app/modules/significant-terms/store/types';
import notTrainModel1 from 'assets/images/notTrainModel1.svg';
import notTrainModel2 from 'assets/images/notTrainModel2.svg';
import notTrainModel3 from 'assets/images/notTrainModel3.svg';
import React from 'react';

import Card from 'app/common/components/card/card';
import { HttpStatus } from 'app/common/types/http.types';

import Header from 'app/modules/header/header';

import bugResolutionPreview from 'assets/images/dAssessment__bug-resolution__preview.png';
import priorityPreview from 'assets/images/dAssessment__priority__preview.png';
import testingProbabilityPreview from 'assets/images/dAssessment__testing-probability__preview.png';
import filterLoadingPreview from 'assets/images/filter-loading-preview.png';
import ttrPreview from 'assets/images/dAssessment__ttr__preview.png';

import './qa-metrics.page.scss';
import { connect, ConnectedProps } from 'react-redux';

interface State {
	filters: FilterFieldBase[]
}

class QAMetricsPage extends React.Component<PropsFromRedux, State> {

	state = {
		filters: [],
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
	}

	componentDidMount() {
		this.randomImageForNotTrainingModel();

		this.props.updateQAMetricsFilters().then(filters => {
			if (filters && filters.length) {
				this.setState(
					{ filters: [...filters] },
					() => { this.loadData(); },
				);
			}
		});
	}

	loadData = (filters?: FilterFieldBase[]) => {
		this.props.updateQAMetricsData(filters || this.state.filters);
	};

	loadNewTableData = (pageIndex: number, limit: number) => {
		this.props.updateQAMetricsTable(this.state.filters, limit, (pageIndex - 1) * limit);
	};

	applyFilters = (filters: FilterFieldBase[]) => {
		this.setState(
			{ filters: [...filters] },
			() => { this.loadData(); },
		);
	};

	resetFilters = () => {
		this.loadData([]);

		this.setState({ filters: [] });
		this.props.updateQAMetricsFilters().then(filters => {
			if (filters) {
				this.setState({ filters: [...filters] });
			}
		});
	};

	render() {
		let style = this.props.isModelTrained ? {} : { filter: `blur(3px)` };

		return (
			<div className="qa-metrics-page">
				<Header pageTitle="QA Metrics" />

				{
					!this.props.isModelTrained &&
          <div className="qa-metrics-page__collecting-data collecting-data">
              <div className="collecting-data__message">
                  Can't calculate predictions. Please train models.
              </div>

              <img src={this.imageForNotTrainingModel} alt="Can't calculate predictions" />
          </div>
				}

				<div className="qa-metrics-page__content">
					<div className="qa-metrics-page__column qa-metrics-page__column_position_left" style={style}>
						<Card
							previewImage={filterLoadingPreview}
							status={this.props.statuses.filters}
							className="qa-metric-filters qa-metrics-page__card"
						>
							{
								this.state.filters.length > 0 &&
                <Filters
                    filters={this.state.filters}
                    applyFilters={this.applyFilters}
                    resetFilters={this.resetFilters}
                />
							}
						</Card>

						<Card
							previewImage={testingProbabilityPreview} title="Area Of Testing Probability"
							status={this.props.statuses.data}
							className="probability qa-metrics-page__card"
						>
							<TagCloud tags={this.props.areas_of_testing_chart as Terms} />
						</Card>

					</div>

					<div className="qa-metrics-page__column qa-metrics-page__column_position_right" style={style}>
						<Card
							previewImage={bugResolutionPreview} title="Bug Resolution"
							status={this.props.statuses.data}
							className="bug-resolution qa-metrics-page__card"
							hoverHeader
						>
							<div className="bug-resolution__charts">

								{
									Object.values(this.props.resolution_chart).map((data, index) => (
										<DonutChart
											key={index}
											className="bug-resolution__chart"
											data={data as DonutChartData}
											colorSchema={index % 2 === 0 ? DonutChartColorSchemes.greenBlue : DonutChartColorSchemes.orangeViolete}
										/>
									))
								}
							</div>
						</Card>

						<Card
							previewImage={priorityPreview} title="Priority"
							status={this.props.statuses.data}
							className="priority qa-metrics-page__card"
						>
							<CustomBarChart data={this.props.priority_chart as DonutChartData} />
						</Card>

						<Card
							previewImage={ttrPreview} title="Time to Resolve (TTR)"
							status={this.props.statuses.data}
							className="ttr qa-metrics-page__card"
						>
							<CustomBarChart
								data={this.props.ttr_chart as DonutChartData}
								verticalDirection
								multiColors
								percentage
							/>
						</Card>
					</div>
				</div>

				{
					this.props.statuses.data === HttpStatus.FINISHED &&
          <div className="qa-metrics-page__content" style={style}>
              <Card
                  title="Predictions Table"
                  className="qa-metrics-page__predictions-table qa-metrics-page__card"
                  hoverHeader
              >
								{
									this.props.statuses.table === HttpStatus.RELOADING &&
                  <CircleSpinner alignCenter />
								}

                  <PredictionsTable
                      tableData={this.props.predictions_table}
                      totalCount={this.props.prediction_table_rows_count}
                      onChangePage={this.loadNewTableData}
                  />
              </Card>
          </div>
				}
			</div>
		);
	}
}

const mapStateToProps = (state: RootStore) => ({
	isModelTrained: state.qaMetricsPage.isModelTrained,
	statuses: state.qaMetricsPage.statuses,
	predictions_table: state.qaMetricsPage.predictions_table,
	prediction_table_rows_count: state.qaMetricsPage.prediction_table_rows_count,
	areas_of_testing_chart: state.qaMetricsPage.areas_of_testing_chart,
	priority_chart: state.qaMetricsPage.priority_chart,
	ttr_chart: state.qaMetricsPage.ttr_chart,
	resolution_chart: state.qaMetricsPage.resolution_chart,
});

const mapDispatchToProps = {
	updateQAMetricsFilters,
	updateQAMetricsData,
	updateQAMetricsTable,
};

const connector = connect(
	mapStateToProps,
	mapDispatchToProps,
);

type PropsFromRedux = ConnectedProps<typeof connector>

export default connector(QAMetricsPage);
