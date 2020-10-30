import { AnalysisAndTrainingDefectSubmission } from "app/common/types/analysis-and-training.types";
import React from "react";
import cn from "classnames";

import "./defect-submission.scss";
import Tooltip from "app/common/components/tooltip/tooltip";

const TimeFilters = {
	Day: "Day",
	Weeks: "Week",
	Months: "Month",
	ThreeMonths: "3 Months",
	SixMonths: "6 Months",
	Year: "Year",
};

interface Props {
	defectSubmission: AnalysisAndTrainingDefectSubmission | undefined;
	activeTimeFilter: string;
	onChangePeriod: (period: string) => void;
}

type LineCoordinateTemplate = {
	startLineX: number;
	endLineX: number;
	startLineY: number;
	endLineY: number;
};

type GraphLinePoint = { data: string; createdValue: number; resolvedValue: number };

class DefectSubmission extends React.Component<Props> {
	maxValue = 0;
	minValue = 0;
	segmentWidth = 120;
	yAxisBarWidth = 70;
	yAxisSteps = 7;
	scrollableGraphWidth = 0;
	potentialGraphHeight: number | undefined;
	graphData: GraphLinePoint[] = [];

	graphTooltipRef: React.RefObject<HTMLDivElement> = React.createRef();
	graphPointerRef: React.RefObject<HTMLDivElement> = React.createRef();
	graphRef: React.RefObject<HTMLDivElement> = React.createRef();

	pointerCoordinates: number[] = [0, 0];
	tooltipCoordinates: number[] = [0, 0];

	colorSchema: string[] = ["#E61A1A", "#33CC99"];

	constructor(props: Props) {
		super(props);

		if (!this.props.defectSubmission) return;

		this.graphData = Object.entries(this.props.defectSubmission.created_line).map(
			([data, value]: [string, number]) => ({
				data,
				createdValue: value,
				resolvedValue: this.props.defectSubmission!.resolved_line[data],
			})
		);

		this.minValue = Math.min(this.graphData[0].createdValue, this.graphData[0].resolvedValue);

		const permMaxValue = Math.max(
			this.graphData[this.graphData.length - 1].createdValue,
			this.graphData[this.graphData.length - 1].resolvedValue
		);
		const tickInterval = this.getYAxisTick(permMaxValue, this.yAxisSteps);
		this.yAxisSteps = Math.ceil(permMaxValue / tickInterval);
		this.maxValue = tickInterval * this.yAxisSteps;

		if (this.maxValue === permMaxValue) {
			this.yAxisSteps += 1;
			this.maxValue += tickInterval;
		}
	}

	setFilter = (timeFilter: string) => () => {
		this.props.onChangePeriod(timeFilter);
	};

	shouldComponentUpdate = () => false;

	componentDidMount = () => {
		const svgElem: any = this.graphRef.current?.getElementsByClassName(
			"defect-submission__graph-svg"
		);
		const svgWrapper = this.graphRef.current?.getElementsByClassName("defect-submission__graph");

		if (svgElem && svgElem[0] && svgWrapper && svgWrapper[0]) {
			const wrapperWidth = (svgWrapper.item(0) as HTMLDivElement).offsetWidth;

			if (wrapperWidth > this.segmentWidth * this.graphData.length)
				this.segmentWidth = (0.975 * wrapperWidth) / (this.graphData.length - 1 || 2);

			this.scrollableGraphWidth =
				(this.graphData.length - 1
					? (this.graphData.length - 1) * this.segmentWidth
					: this.segmentWidth * 2) + 10;

			this.potentialGraphHeight = svgElem.item(0).height.baseVal.value;
			this.forceUpdate();
		}
	};

	displayPoint = (coords: number[], colorIndex: number) => {
		if (
			!this.graphPointerRef.current ||
			(coords[0] === this.pointerCoordinates[0] && coords[1] === this.pointerCoordinates[1])
		)
			return;

		this.pointerCoordinates = [...coords];

		this.graphPointerRef.current.style.cssText = `left: ${coords[0]}px; top: ${coords[1]}px; background: ${this.colorSchema[colorIndex]}; display: flex`;
	};

	displayTooltip = (coords: number[], dataIndex: number, lineIndex: number) => {
		if (
			!this.graphTooltipRef.current ||
			(coords[0] === this.tooltipCoordinates[0] && coords[1] === this.tooltipCoordinates[1])
		)
			return;

		this.tooltipCoordinates = [...coords];

		const dataField = lineIndex === 0 ? "createdValue" : "resolvedValue";

		this.graphTooltipRef.current.children[0].innerHTML = `${this.graphData[dataIndex][dataField]}`;
		this.graphTooltipRef.current.style.cssText = `left: ${coords[0] - 15}px; top: ${
			coords[1] - 5
		}px;`;
	};

	euclideanDistance = (x1: number, y1: number, x2: number, y2: number) =>
		Math.hypot(x2 - x1, y2 - y1);

	getClosestPointToMouse = (x: number, y: number, coordsArr: LineCoordinateTemplate[]) => {
		let minDistanceArr: number[] = [];
		let minDistance = Infinity;
		let minDistanceLineIndex = 0;
		let minDistanceLineEndIndex = 0;

		const distanceCalculator = (
			pointX: number,
			pointY: number,
			lineIndex: number,
			endIndex: number
		) => {
			const distanceArr = [pointX, pointY];
			const distance = this.euclideanDistance(x, y, pointX, pointY);
			if (minDistance > distance) {
				minDistance = distance;
				minDistanceArr = [...distanceArr];
				minDistanceLineIndex = lineIndex;
				minDistanceLineEndIndex = endIndex;
			}
		};
		coordsArr.forEach((item, index) => {
			distanceCalculator(item.startLineX, item.startLineY, index, 0);
			distanceCalculator(item.endLineX, item.endLineY, index, 1);
		});

		return { minDistanceArr, minDistanceLineIndex, minDistanceLineEndIndex };
	};

	mouseEnterDisplayTooltip = (e: any, coordsArr: LineCoordinateTemplate[], index: number) => {
		const rect = e.target.getBoundingClientRect();
		const minDistanceObject = this.getClosestPointToMouse(
			e.clientX - rect.x + this.segmentWidth * index,
			e.clientY - rect.y,
			coordsArr
		);
		this.displayPoint(minDistanceObject.minDistanceArr, minDistanceObject.minDistanceLineIndex);
		this.displayTooltip(
			minDistanceObject.minDistanceArr,
			index + minDistanceObject.minDistanceLineEndIndex,
			minDistanceObject.minDistanceLineIndex
		);
	};

	buildGraphObject = (
		startLineY: number,
		endLineY: number,
		lineIndex: number,
		segmentIndex: number,
		objectType: "line" | "circle",
		coordinateArr: LineCoordinateTemplate[]
	) => {
		if (
			!this.potentialGraphHeight ||
			segmentIndex === this.graphData.length ||
			(objectType === "line" && segmentIndex === 0)
		)
			return null;

		const endXCoordinate =
			objectType === "line" ? segmentIndex * this.segmentWidth + 5 : this.scrollableGraphWidth / 2;
		const startPositionHorizontalShift = objectType === "line" ? this.segmentWidth : 0;

		const coordinates: LineCoordinateTemplate = {
			startLineX: endXCoordinate - startPositionHorizontalShift - 3,
			endLineX: endXCoordinate - 3,
			startLineY: this.potentialGraphHeight - startLineY,
			endLineY: this.potentialGraphHeight - endLineY,
		};

		coordinateArr.push(coordinates);

		if (objectType === "line")
			return (
				<path
					d={`M${coordinates.startLineX} ${coordinates.startLineY} L${coordinates.endLineX} ${coordinates.endLineY}`}
					className="line-chart__graph-line"
					stroke={this.colorSchema[lineIndex]}
				/>
			);

		return (
			<circle
				cx={coordinates.startLineX + 1.5}
				cy={coordinates.startLineY}
				r={2}
				fill={this.colorSchema[lineIndex]}
				className="line-chart__circle"
			/>
		);
	};

	renderGraphLine = (index: number) => {
		if (!this.potentialGraphHeight || index === this.graphData.length) return null;
		const pointHeight = this.potentialGraphHeight / this.maxValue;

		const endXCoordinate = index * this.segmentWidth + 5;

		const textAnchor =
			// eslint-disable-next-line no-nested-ternary
			index === 0 ? "start" : index === this.graphData.length - 1 ? "end" : "middle";

		const coordinateArr: LineCoordinateTemplate[] = [];
		const createdLine = this.buildGraphObject(
			this.graphData[index - 1]?.createdValue * pointHeight,
			this.graphData[index]?.createdValue * pointHeight,
			0,
			index,
			"line",
			coordinateArr
		);
		const resolvedLine = this.buildGraphObject(
			this.graphData[index - 1]?.resolvedValue * pointHeight,
			this.graphData[index]?.resolvedValue * pointHeight,
			1,
			index,
			"line",
			coordinateArr
		);

		return (
			<React.Fragment key={index}>
				{index !== 0 && (
					<>
						<rect
							x={endXCoordinate - this.segmentWidth}
							width={this.segmentWidth}
							height={this.potentialGraphHeight}
							className="line-chart__rect"
							onMouseMove={(e: any) =>
								this.mouseEnterDisplayTooltip(e, [...coordinateArr], index - 1)
							}
						/>
						{resolvedLine}
						{createdLine}
					</>
				)}

				<text
					x={endXCoordinate}
					y={this.potentialGraphHeight}
					textAnchor={textAnchor}
					className="line-chart__axis-text"
				>
					{this.graphData[index].data}
				</text>
				<line
					x1={endXCoordinate}
					x2={endXCoordinate}
					y1={0}
					y2={this.potentialGraphHeight}
					className="line-chart__vertical-line"
				/>
			</React.Fragment>
		);
	};

	renderGraphPoint = () => {
		if (!this.potentialGraphHeight) return null;

		const endXCoordinate = this.scrollableGraphWidth / 2;

		const pointHeight = this.potentialGraphHeight / this.maxValue;

		const coordinateArr: LineCoordinateTemplate[] = [];
		const createdCircle = this.buildGraphObject(
			this.graphData[0]?.createdValue * pointHeight,
			this.graphData[0]?.createdValue * pointHeight,
			0,
			0,
			"circle",
			coordinateArr
		);
		const resolvedCircle = this.buildGraphObject(
			this.graphData[0]?.resolvedValue * pointHeight,
			this.graphData[0]?.resolvedValue * pointHeight,
			1,
			0,
			"circle",
			coordinateArr
		);

		return (
			<>
				<rect
					x={3}
					width={this.scrollableGraphWidth}
					height={this.potentialGraphHeight}
					onMouseMove={(e: any) => this.mouseEnterDisplayTooltip(e, [...coordinateArr], 0)}
					className="line-chart__rect"
				/>

				<text
					x={endXCoordinate}
					y={this.potentialGraphHeight}
					textAnchor="middle"
					className="line-chart__axis-text"
				>
					{this.graphData[0].data}
				</text>

				<line
					x1={endXCoordinate}
					x2={endXCoordinate}
					y1={0}
					y2={this.potentialGraphHeight}
					className="line-chart__vertical-line"
				/>

				{createdCircle}
				{resolvedCircle}
			</>
		);
	};

	getYAxisTick = (range: number, targetSteps: number) => {
		const tempStep = range / targetSteps;

		const mag = Math.floor(Math.log(tempStep) / Math.LN10);
		// eslint-disable-next-line no-restricted-properties
		const magPow = Math.pow(10, mag);

		let magMsd = Math.round(tempStep / magPow + 0.5);

		if (magMsd > 5) magMsd = 10;
		else if (magMsd > 2) magMsd = 5;
		else if (magMsd > 1) magMsd = 2;

		return magMsd * magPow;
	};

	renderYAxis = () => {
		if (!this.potentialGraphHeight) return null;

		const steps = 7;

		const beautifulTick = Math.ceil(this.getYAxisTick(this.maxValue, steps));

		const beautifulSteps = Math.round(this.maxValue / beautifulTick);

		const yAxis = [];

		for (let i = 0; i <= beautifulSteps; i += 1)
			yAxis.push(
				<text
					key={i}
					x={this.yAxisBarWidth - 20}
					y={(this.potentialGraphHeight - 10) * (1 - (1 / beautifulSteps) * i) - 10}
					textAnchor="end"
					className="line-chart__axis-text"
				>
					{beautifulTick * i}
				</text>
			);

		return yAxis;
	};

	render() {
		const { activeTimeFilter } = this.props;
		const graphHeight = Number(this.graphRef.current?.offsetHeight) - 5 || "calc( 100% - 25px )";

		return (
			<div className="defect-submission">
				<div className="defect-submission-legend">
					<div className="defect-submission-legend__wrapper">
						<div
							className={cn(
								"defect-submission-legend__point",
								"defect-submission-legend__point_created"
							)}
						 />
						<p className="defect-submission-legend__title">
							Created issues - {this.props.defectSubmission?.created_total_count}
						</p>
					</div>
					<div className="defect-submission-legend__wrapper">
						<div
							className={cn(
								"defect-submission-legend__point",
								"defect-submission-legend__point_resolved"
							)}
						 />
						<p className="defect-submission-legend__title">
							Resolved issues - {this.props.defectSubmission?.resolved_total_count}
						</p>
					</div>
				</div>

				<div className="defect-submission__scroll-container" ref={this.graphRef}>
					<div>
						<svg width={this.yAxisBarWidth} height="100%">
							{this.renderYAxis()}
						</svg>
					</div>

					<div className="defect-submission__graph">
						<div>
							<Tooltip message="" duration={0} tooltipOuterRef={this.graphTooltipRef}>
								<div
									className={cn(
										"defect-submission__graph-pointer",
										"defect-submission__graph-pointer_created"
									)}
									ref={this.graphPointerRef}
								 />
							</Tooltip>

							<svg
								width={this.scrollableGraphWidth}
								height={graphHeight}
								className="defect-submission__graph-svg"
							>
								{this.graphData.length === 1
									? this.renderGraphPoint()
									: this.graphData.map((item, index) => this.renderGraphLine(index))}
							</svg>
						</div>
					</div>
				</div>

				<ul className="defect-submission__filter">
					{Object.values(TimeFilters).map((val: string) => (
						<li
							key={val}
							onClick={this.setFilter(val)}
							className={cn(
								"defect-submission__period",
								activeTimeFilter === val && "defect-submission__period_active"
							)}
						>
							{val}
						</li>
					))}
				</ul>
			</div>
		);
	}
}

export default DefectSubmission;
