import { AnalysisAndTrainingStatistic, StatisticPart } from 'app/common/types/analysis-and-training.types';
import React from 'react';

import './statistic.scss';

interface Props {
	statistic: AnalysisAndTrainingStatistic
}

class Statistic extends React.Component<Props> {

	renderTableSection = (sectionName: string, index: number) => {
		let sectionObject: StatisticPart = this.props.statistic[sectionName];
		return (
			<tr className="statistic-table__row" key={index}>
				<td className="statistic-table__row-header">{sectionName}</td>
				<td className="statistic-table__cell statistic-table__cell_type_max">{sectionObject.maximum}</td>
				<td className="statistic-table__cell statistic-table__cell_type_min">{sectionObject.minimum}</td>
				<td className="statistic-table__cell statistic-table__cell_type_mean">{sectionObject.mean}</td>
				<td className="statistic-table__cell statistic-table__cell_type_std">{sectionObject.std}</td>
			</tr>
		)
	}

	render() {
		return (
			<table className="statistic-table">
				<thead>
				<tr className="statistic-table__row">
					<th className="statistic-table__row-header">{/*angle cell*/}</th>
					<th className="statistic-table__column-header">MAX</th>
					<th className="statistic-table__column-header">MIN</th>
					<th className="statistic-table__column-header">MEAN</th>
					<th className="statistic-table__column-header">STD</th>
				</tr>
				</thead>

				<tbody>
				{
					Object.keys(this.props.statistic).map((item: string,index: number)=>this.renderTableSection(item, index))
				}
				</tbody>
			</table>
		);
	}
}

export default Statistic;
