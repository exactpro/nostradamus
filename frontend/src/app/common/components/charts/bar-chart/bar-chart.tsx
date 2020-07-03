import React, { CSSProperties, RefObject } from 'react';
import cn from 'classnames';

import 'app/common/components/charts/bar-chart/bar-chart.scss';

interface IProps {
	percentage: boolean;
	data: BarChartData;
	verticalDirection: boolean;
	multiColors: boolean;
}

interface IState {
	maxChartSize: number;
}

type BarChartData = {
	[key: string]: number
}

export type BarChartColumn = {
	value: number,
	label: string,
}

const colorSchema = [
	"#5798D9",
	"#F2D16D",
	"#FFA666",
	"#F53D3D",
];

export class CustomBarChart extends React.Component<IProps, IState> {

	chartAreaRef: RefObject<HTMLDivElement>;

	static defaultProps = {
		percentage: false,
		verticalDirection: false,
		multiColors: false
	};

	state = {
		maxChartSize: 0
	};

	constructor(props: IProps) {
		super(props);

		this.chartAreaRef = React.createRef();
	}

	componentDidMount(): void {
		if (this.chartAreaRef.current) {
			let size = this.props.verticalDirection ?
				this.chartAreaRef.current.offsetHeight - 30 :
				this.chartAreaRef.current.offsetWidth - 80;

			this.setState({
				maxChartSize: size
			});
		}
	}

	render() {
		let data: BarChartColumn[] = Object.entries(this.props.data)
			.map(([columnName, value]) => ({
				label: columnName,
				value,
			}));

		let maxValue = 0, minValue = data[0].value;

		data.forEach((item) => {
			if (item.value > maxValue) maxValue = item.value;
			if (item.value < minValue) minValue = item.value;
		});

		return (
			<div className={cn("bar-chart", { "bar-chart_vertical": this.props.verticalDirection })}>
				{
					data.map(((item, index) =>{
							let style: CSSProperties = {};

							if (this.props.verticalDirection) {
								style.height = item.value/maxValue * this.state.maxChartSize;
							} else {
								style.width = item.value/maxValue * this.state.maxChartSize
							}

							if (this.props.multiColors) {
								style.backgroundColor = colorSchema[index];
							}

							return (
								<div className="bar-chart__item" key={item.label}>
									<div className="bar-chart__item-label">
										{item.label}
									</div>

									<div className="bar-chart__item-chart" ref={this.chartAreaRef}>
										{
											!!item.value &&
											<div className="bar-chart__item-rectangle" style={style}>
												{/*graph*/}
											</div>
										}

										<div className="bar-chart__item-value">
											{item.value} {this.props.percentage && '%'}
										</div>
									</div>
								</div>
							)}
					))
				}
			</div>
		);
	}

}
