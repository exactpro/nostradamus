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
	color: string,
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

	constructor(props: IProps){
		super(props);
		 
		this.data = 
			Object.entries(this.props.data)
			.map(([sectorName, value], index) => ({
				label: sectorName,
				id: sectorName,
				value: Math.round(value),
				color: this.props.colorSchema![index]
			}));
	}
 
	data: DonutChartSector[] = [];
	pieRef: React.RefObject<HTMLDivElement> = React.createRef(); 

	getMidAngle = (segmentId: string) => {
		let midAngle: number = 0; 
		const percentageRadian: number = Math.PI/50;
		for(let i of this.data){
			if(i.id === segmentId){
				midAngle+=percentageRadian*i.value/2;
				break;
			}
			midAngle+=percentageRadian*i.value; 
		}

		return midAngle;
	}

	shiftDonutSegment = (segmentId: string, target: SVGClipPathElement ,dl: number = 2) => {

		const midAngle = this.getMidAngle(segmentId); 
		const dx = dl*Math.cos(midAngle);
		const dy = -dl*Math.sin(midAngle); 

		target.style.transform=`translate(${dx}px,${dy}px)`;
	}

	pieMouseEnterEffect = ({id, label ,value, color}: any, {target}: any) => {  
		
		if(value !== 100) this.shiftDonutSegment(id, target, 3);

		this.setState({
			isPercentageDataVisible: true,
			percentageData:{ value, color }});
	}
	
	pieMouseLeaveEffect = ({id, value}: any, {target}: any) => { 
		if(value !== 100) this.shiftDonutSegment(id, target, 0);

		this.setState({
			isPercentageDataVisible: false,
			percentageData:{
				value: 0,
				color: "#FFFFFF"}
			});
	}; 

	render() { 
		
		let chartData = this.data.filter(item=>item.value!==0);

		return (
			<div className={cn('donut-chart', this.props.className)}>
				{/*legend*/}
				<div className="donut-chart-legend">
					{
						this.data.map((item, index)=> {
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
				<div className="donut-chart-wrapper" ref={this.pieRef}>
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
						colors={chartData.map(item=>item.color)}
						data={chartData}
						innerRadius={0.65}
						padAngle={4}
						startAngle={90}
						endAngle={-270}
						sortByValue={false}
						cornerRadius={5}
						enableSlicesLabels={false}
						enableRadialLabels={false}
						animate={true}
						margin={ { left: 5, right: 5, top: 5, bottom: 5 } }
						theme={{ tooltip: { container: { display: "none" } } } }
					/>
				</div>
			</div>
		);
	}
}

export default DonutChart;
