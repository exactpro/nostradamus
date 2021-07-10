import { ChartData } from "app/common/components/charts/types";
import React, { CSSProperties, ReactElement, RefObject } from "react";
import cn from "classnames";

import "app/common/components/charts/bar-chart/bar-chart.scss";

interface IProps {
	percentage: boolean;
	data: ChartData;
	verticalDirection: boolean;
	multiColors: boolean;
}

interface IState {
	maxChartSize: number;
}

export type BarChartColumn = {
	value: number;
	label: string;
};

const colorSchema = ["#5798D9", "#F2D16D", "#FFA666", "#F53D3D"];

export class CustomBarChart extends React.Component<IProps, IState> {
	chartAreaRef: RefObject<HTMLDivElement>;

	// eslint-disable-next-line react/static-property-placement
	static defaultProps = {
		percentage: false,
		verticalDirection: false,
		multiColors: false,
	};

	constructor(props: IProps) {
		super(props);

		this.chartAreaRef = React.createRef();
		this.state = { maxChartSize: 0 };
	}

	componentDidMount(): void {
		const { props } = this;

		if (this.chartAreaRef.current) {
			const size = props.verticalDirection
				? this.chartAreaRef.current.offsetHeight - 30
				: this.chartAreaRef.current.offsetWidth - 80;

			this.setState({
				maxChartSize: size,
			});
		}
	}

	render(): ReactElement {
		const { props, state } = this;
		const { data } = props;

		let maxValue = 0;
		let minValue = data[0].value;

		data.forEach((item) => {
			if (item.value > maxValue) maxValue = item.value;
			if (item.value < minValue) minValue = item.value;
		});

		return (
			<div className={cn("bar-chart", { "bar-chart_vertical": props.verticalDirection })}>
				{data.map((item, index) => {
					const style: CSSProperties = {};

					if (props.verticalDirection) {
						style.height = (item.value / maxValue) * state.maxChartSize;
					} else {
						style.width = (item.value / maxValue) * state.maxChartSize;
					}

					if (props.multiColors) {
						style.backgroundColor = colorSchema[index];
					}

					return (
						<div className="bar-chart__item" key={item.name}>
							<div className="bar-chart__item-label">{item.name}</div>

							<div className="bar-chart__item-chart" ref={this.chartAreaRef}>
								{!!item.value && (
									<div className="bar-chart__item-rectangle" style={style}>
										{/* graph */}
									</div>
								)}

								<div className="bar-chart__item-value">
									{item.value} {props.percentage && "%"}
								</div>
							</div>
						</div>
					);
				})}
			</div>
		);
	}
}
