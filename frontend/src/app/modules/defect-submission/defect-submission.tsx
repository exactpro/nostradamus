import { AnalysisAndTrainingDefectSubmission } from 'app/common/types/analysis-and-training.types';
import React from 'react';
import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import cn from 'classnames';

import './defect-submission.scss';

const TimeFilters = {
	Day: 'Day',
	Weeks: 'Week',
	Months: 'Month',
	ThreeMonths: '3 Months',
	SixMonths: '6 Months',
	Year: 'Year',
};

interface Props {
	defectSubmission: AnalysisAndTrainingDefectSubmission | undefined,
	activeTimeFilter: string,
	onChangePeriod: (period: string) => void
}

class DefectSubmission extends React.Component<Props> {

	graphRef: React.RefObject<HTMLDivElement> = React.createRef();

	setFilter = (timeFilter: string) => () => {
		this.props.onChangePeriod(timeFilter);
	};

	render() {
		let { activeTimeFilter } = this.props;

		const graphData = Object.entries(this.props.defectSubmission || {}).map(([key, value]) => ({
			data: key,
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

export default DefectSubmission;
