import { updateDefectSubmission } from 'app/common/store/analysis-and-training/thunks';
import { RootStore } from 'app/common/types/store.types';
import React from 'react';
import { connect, ConnectedProps } from 'react-redux';
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import cn from 'classnames';
import moment from 'moment';

import './defect-submission.scss';

const TimeFilters = {
	Day: 'Day',
	Weeks: 'Week',
	Months: 'Month',
	ThreeMonths: '3 Months',
	SixMonths: '6 Months',
	Year: 'Year',
};

interface DefectSubmissionState {
	activeTimeFilter: string
}

class DefectSubmission extends React.Component<PropsFromRedux, DefectSubmissionState> {

	state = {
		activeTimeFilter: TimeFilters.SixMonths,
	};

	graphRef: React.RefObject<HTMLDivElement> = React.createRef();

	setFilter = (timeFilter: string) => () => {
		this.setState({
			...this.state,
			activeTimeFilter: timeFilter,
		}, this.updateGraph);
	};

	updateGraph = () => {
		this.props.updateDefectSubmission(this.state.activeTimeFilter);
	};

	componentDidMount(): void {
		this.updateGraph();
	}

	render() {
		let { activeTimeFilter } = this.state;

		const graphData = Object.entries(this.props.defectSubmission || {}).map(([key, value]) => ({
			data: moment(key).format('DD.MM.YYYY'),
			value: value,
		}));

		let yAxisBarWidth: number = 70;

		let potentialGraphWidth = this.graphRef.current?
															this.graphRef.current.offsetWidth - yAxisBarWidth - 5:
															undefined;

		let scrollableGraphWidth = graphData.length * 120;

		return (
			<div className="defect-submission">
				<div className="defect-submission__scroll-container" ref={this.graphRef}>
					<ResponsiveContainer width={yAxisBarWidth} height="100%" className="defect-submission__helper-graph">
						<LineChart data={graphData}>
							<CartesianGrid fill="#E5F2F9" horizontal={false} stroke="#FFFFFF" style={{display: 'none'}} />
							<XAxis axisLine={false} tickLine={false} dataKey="data" tickMargin={15}  />
							<YAxis axisLine={false}
							       tickLine={false}
							       tickMargin={10}
							       domain={['dataMin', 'dataMax+100']}
							       type="number" scale="linear"
							       interval="preserveStart"
							/>
							<Line dataKey="value" strokeWidth={4} stroke="#E61A1A" dot={false} width={0} style={{display: 'none'}}/>
						</LineChart>
					</ResponsiveContainer>

					<div className="defect-submission__graph">
						<ResponsiveContainer width={potentialGraphWidth && scrollableGraphWidth<potentialGraphWidth? potentialGraphWidth: scrollableGraphWidth} height="100%">
							<LineChart data={graphData}>
								<CartesianGrid fill="#E5F2F9" horizontal={false} stroke="#FFFFFF" />
								<XAxis axisLine={false} tickLine={false} dataKey="data" tickMargin={15} interval="preserveStartEnd" />
								<YAxis axisLine={false}
								       tickLine={false}
								       hide={true}
								       tickMargin={10}
								       domain={['dataMin', 'dataMax+100']}
								       type="number" scale="linear"
								       interval="preserveStartEnd"
								/>
								<Tooltip />
								<Line dataKey="value" strokeWidth={4} stroke="#E61A1A" dot={false} />
							</LineChart>
						</ResponsiveContainer>
					</div>
				</div>

				<ul className="defect-submission__filter">
					{
						Object.values(TimeFilters).map((val: string) => (
							<li
								key={val}
								onClick={this.setFilter(val)}
								className={cn('defect-submission__period', activeTimeFilter === val && 'defect-submission__period_active')}
							>
								{val}
							</li>
						))
					}
				</ul>
			</div>
		);
	}
}

const mapStateToProps = (state: RootStore) => ({
	defectSubmission: state.analysisAndTraining.analysisAndTraining.defectSubmission,
});

const mapDispatchToProps = {
	updateDefectSubmission,
};

const connector = connect(
	mapStateToProps,
	mapDispatchToProps,
);

type PropsFromRedux = ConnectedProps<typeof connector>

export default connector(DefectSubmission);

// const data = [
// 	{
// 		'name': '31.08',
// 		'pv': 200,
// 	},
// 	{
// 		'name': '01.09',
// 		'pv': 260,
// 	},
// ];
