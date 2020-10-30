import {
	AnalysisAndTrainingStatistic,
	StatisticPart,
} from "app/common/types/analysis-and-training.types";
import React from "react";

import "./statistic.scss";

interface Props {
	statistic: AnalysisAndTrainingStatistic;
}

function Statistic(props: Props) {
	const statisticColumnKeys = Object.keys(Object.values(props.statistic)[0]);

	return (
		<table className="statistic-table">
			<thead>
				<tr className="statistic-table__row">
					<th className="statistic-table__row-header">{/* angle cell */}</th>
					{statisticColumnKeys.map((columnName, index) => (
						<th key={index} className="statistic-table__column-header">
							{columnName.toUpperCase()}
						</th>
					))}
				</tr>
			</thead>

			<tbody>
				{Object.keys(props.statistic).map((sectionName: string, sectionIndex: number) => {
					const sectionObject: StatisticPart = props.statistic[sectionName];

					return (
						<tr className="statistic-table__row" key={sectionIndex}>
							<td className="statistic-table__row-header">{sectionName}</td>
							{statisticColumnKeys.map((columnName, index) => (
								<td key={index} className="statistic-table__cell">
									{sectionObject[columnName]}
								</td>
							))}
						</tr>
					);
				})}
			</tbody>
		</table>
	);
}

export default Statistic;
