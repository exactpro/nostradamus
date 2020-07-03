import React from 'react';
import cn from 'classnames';
import { connect, ConnectedProps } from 'react-redux';
import { RootStore } from 'app/common/types/store.types';

import mainStatisticArrow from 'assets/icons/main-statistic-arrow.icon.svg';

import './main-statistic.scss';

interface MainStatisticProps {
	className?: string
}

class MainStatistic extends React.Component<Props> {

	render() {
		return (
			<div className={cn('main-statistic', this.props.className)}>
				<div className="main-statistic__block">
					<div className="main-statistic__number main-statistic__number_type_total">{this.props.total}</div>
					<div className="main-statistic__number-label">bugs uploaded</div>
				</div>

				<img className="main-statistic__block" src={mainStatisticArrow} alt="arrow icon" />

				<div className="main-statistic__block">
					<div className="main-statistic__number main-statistic__number_type_filtered">{this.props.filtered}</div>
					<div className="main-statistic__number-label">bugs filtered</div>
				</div>
			</div>
		);
	}
}

const mapStateToProps = (state: RootStore) => ({
	total: state.analysisAndTraining.mainStatistic.total,
	filtered: state.analysisAndTraining.mainStatistic.filtered,
});

const connector = connect(
	mapStateToProps,
);

type PropsFromRedux = ConnectedProps<typeof connector>

type Props = PropsFromRedux & MainStatisticProps;

export default connector(MainStatistic);
