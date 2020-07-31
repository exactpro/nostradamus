import React from 'react';
import cn from 'classnames';

import mainStatisticArrow from 'assets/icons/main-statistic-arrow.icon.svg';

import './main-statistic.scss';

export interface MainStatisticData {
	total: number,
	filtered: number,
}

interface Props {
	className?: string,
	statistic: MainStatisticData
}

class MainStatistic extends React.Component<Props> {

	static defaultProps = {
		statistic: {
			total: 0,
			filtered: 0,
		},
	};

	render() {

		return (
			<div className={cn('main-statistic', this.props.className)}>
				<div className="main-statistic__block">
					<div className="main-statistic__number main-statistic__number_type_total">{this.props.statistic.total}</div>
					<div className="main-statistic__number-label">bugs uploaded</div>
				</div>

				<img className="main-statistic__block" src={mainStatisticArrow} alt="arrow icon" />

				<div className="main-statistic__block">
					<div className="main-statistic__number main-statistic__number_type_filtered">{this.props.statistic.filtered}</div>
					<div className="main-statistic__number-label">bugs filtered</div>
				</div>
			</div>
		);
	}
}

export default MainStatistic;
