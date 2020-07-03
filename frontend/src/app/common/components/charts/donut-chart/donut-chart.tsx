import React, { RefObject } from 'react';
import { ResponsivePie } from '@nivo/pie';
import cn from 'classnames';

import 'app/common/components/charts/donut-chart/donut-chart.scss';

export const DonutChartColorSchemes = {
	greenBlue: ['#33CC99', '#5CADD6'],
	orangeViolete: ['#FFA666', '#BCAAF2'],
};

export type DonutChartData = {
	[key: string]: number
}

export type DonutChartSector = {
	value: number,
	label: string,
	id: string,
}

interface IProps {
	className?: string;
	colorSchema?: string[];
	data: DonutChartData;
}

interface iState {
	width: number;
}

class DonutChart extends React.Component<IProps, iState> {

	static defaultProps = {
		colorSchema: DonutChartColorSchemes.greenBlue,
	};

	chartRef: RefObject<HTMLDivElement>;

	state = {
		width: 0,
	};

	constructor(props: IProps) {
		super(props);

		this.chartRef = React.createRef();
	}

	componentDidMount() {
		if (!this.state.width && this.chartRef.current) {

			this.setState({
				width: Number(this.chartRef.current.offsetHeight),
			});
		}
	}

	render() {
		let data: DonutChartSector[] = Object.entries(this.props.data)
			.map(([sectorName, value]) => ({
				label: sectorName,
				id: sectorName,
				value,
			}));

		return (
			<div className={cn('donut-chart', this.props.className)} ref={this.chartRef}>
				{/*legend*/}
				<div className="donut-chart__legend">
					<ResponsivePie
						colors={this.props.colorSchema}
						data={data}
						innerRadius={0.7}
						padAngle={4}
						startAngle={90}
						endAngle={-270}
						sortByValue={false}
						cornerRadius={5}
						enableSlicesLabels={false}
						enableRadialLabels={false}
						animate={true}
						legends={[
							{
								anchor: 'bottom-left',
								direction: 'column',
								itemWidth: 200,
								itemHeight: 20,
								itemTextColor: '#7E7E7E',
								itemsSpacing: 26,
								symbolSize: 20,
								symbolShape: 'circle',
							},
						]}
					/>
				</div>

				{/*chart*/}
				<div className="donut-chart__chart" style={{ width: this.state.width }}>
					<ResponsivePie
						colors={this.props.colorSchema}
						data={data}
						innerRadius={0.65}
						padAngle={4}
						startAngle={90}
						endAngle={-270}
						sortByValue={false}
						cornerRadius={5}
						enableSlicesLabels={false}
						enableRadialLabels={false}
						animate={true}
					/>
				</div>
			</div>
		);
	}
}

export default DonutChart;
