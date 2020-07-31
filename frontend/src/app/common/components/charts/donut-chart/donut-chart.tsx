import React from 'react';
import { ResponsivePie } from '@nivo/pie';
import cn from 'classnames';

import 'app/common/components/charts/donut-chart/donut-chart.scss';

export const DonutChartColorSchemes = {
	greenBlue: ['#33CC99', '#5CADD6'],
	orangeViolet: ['#FFA666', '#BCAAF2'],
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
	percentageData: {
		value: number,
		color: string,
	},
	isPercentageDataVisible: boolean,
}

class DonutChart extends React.Component<IProps, iState> {

	static defaultProps = {
		colorSchema: DonutChartColorSchemes.greenBlue,
	};

	state = {
		width: 0,
		percentageData: {
			value: 0,
			color: "#FFFFFF"
		},
		isPercentageDataVisible: false,
	};

	timerId: any = 0;

	pieMouseEnterEffect = ({id, label ,value}: any) => {
		if(this.timerId) return;

		let colorIndex = Object.keys(this.props.data).findIndex((item:string)=>item===label);
		
		this.setState({
			isPercentageDataVisible: true,
			percentageData:{
				value: value,
				color: this.props.colorSchema![colorIndex], 
			}});
	}
	
	pieMouseLeaveEffect = () => {
		if(this.timerId) return;
		
		this.setState({
			isPercentageDataVisible: false,
			percentageData:{
				value: 0,
				color: "#FFFFFF"}
			});
	};

	render() {
		let data: DonutChartSector[] = Object.entries(this.props.data)
			.map(([sectorName, value]) => ({
				label: sectorName,
				id: sectorName,
				value,
			}));
			
		return (
			<div className={cn('donut-chart', this.props.className)}>
				{/*legend*/}
				<div className="donut-chart-legend">
					{
						data.map((item, index)=> {
							let bgColor = this.props.colorSchema? this.props.colorSchema[index]: "transparent";
							return( 
								<div className="donut-chart-legend__wrapper" key={index}>
									<div className="donut-chart-legend__circle-pointer" style={{background: bgColor}}></div>
									<span className="donut-chart-legend__title">{item.label}</span>
								</div>)
						})
					}
				</div>

				{/*chart*/}
				<div className="donut-chart-wrapper">
					{
						<p  style={{color: this.state.percentageData.color}} 
							className={cn("donut-chart-wrapper__percentage-block", 
										  {"donut-chart-wrapper__percentage-block_visible": this.state.isPercentageDataVisible})}>
								{this.state.percentageData.value}%
						</p>
					}
					
					<ResponsivePie
						onMouseEnter={this.pieMouseEnterEffect}
						onMouseLeave={this.pieMouseLeaveEffect}
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
						theme={{ tooltip: { container: { display: "none" } } } }
					/>
				</div>
			</div>
		);
	}
}

export default DonutChart;
