import BacklightTextArea from "app/common/components/backlight-textarea/backlight-text-area";
import Button, { ButtonStyled } from "app/common/components/button/button";
import { IconType } from "app/common/components/icon/icon";
import DropdownElement from "app/common/components/native-components/dropdown-element/dropdown-element";
import React from "react";

import "./predict-text.scss";
import { FilterElementType } from "../settings/elements/elements-types";

export interface Keywords {
	Priority: string[];
	resolution: string[];
	areas_of_testing: string[];
}

export interface PredictMetric {
	metric: PredictMetricsName;
	value: string;
}

export type PredictMetricsName = "Priority" | "resolution" | "areas_of_testing";

interface State {
	text: string;
	currentMetricsValue: {
		[key in PredictMetricsName]: string | undefined;
	};
	layoutArr: PredictMetricsName[];
}

interface Props {
	availableMetricsValues: Keywords;
	keywords?: Keywords;
	onChangePredictOption: (predictOption: PredictMetric) => void;
	onPredict: (text: string) => void;
	onClearAll: () => void;
	text: string;
}

class PredictText extends React.Component<Props, State> {
	state = {
		text: "",
		currentMetricsValue: {
			Priority: undefined,
			resolution: undefined,
			areas_of_testing: undefined,
		},
		layoutArr: [],
	};

	componentDidMount() {
		this.setState({
			text: this.props.text
		});
	}

	onChangeText = (text: string) => {
		this.setState({
			text,
			currentMetricsValue: {
				Priority: undefined,
				resolution: undefined,
				areas_of_testing: undefined,
			},
			layoutArr: [],
		});
		this.props.onClearAll();
	};

	predict = () => {
		this.props.onPredict(this.state.text);
	};

	clearAll = () => {
		this.setState({
			text: "",
			currentMetricsValue: {
				Priority: undefined,
				resolution: undefined,
				areas_of_testing: undefined,
			},
			layoutArr: [],
		});

		this.props.onClearAll();
	};

	changeDropdownValue = (option: PredictMetricsName) => (value: any) => {
		const layoutArr: PredictMetricsName[] = [...this.state.layoutArr].filter(
			(item) => item !== option
		);
		layoutArr.push(option);

		this.props.onChangePredictOption({
			metric: option,
			value,
		});

		this.setState({
			currentMetricsValue: {
				...this.state.currentMetricsValue,
				[option]: value || undefined,
			},
			layoutArr,
		});
	};

	clearDropdownValue = (option: PredictMetricsName) => () => {
		this.changeDropdownValue(option)("");
	};

	render() {
		return (
			<div className="predict-text">
				<BacklightTextArea
					text={this.state.text}
					onChangeText={this.onChangeText}
					keywords={this.props.keywords}
					layoutArr={this.state.layoutArr}
				/>

				<div className="predict-text__dropdowns-wrapper">
					<div className="predict-text__dropdown predict-text__resolution">
						<span className="predict-text__dropdown-title">Resolution</span>
						<DropdownElement
							type={
								this.props.availableMetricsValues.resolution.length
									? FilterElementType.simple
									: FilterElementType.disabled
							}
							value={this.state.currentMetricsValue.resolution}
							placeholder="Select"
							writable={false}
							dropDownValues={this.props.availableMetricsValues.resolution}
							onChange={this.changeDropdownValue("resolution")}
							onClear={this.clearDropdownValue("resolution")}
						/>
					</div>

					<div className="predict-text__dropdown predict-text__priority">
						<span className="predict-text__dropdown-title">Priority</span>
						<DropdownElement
							type={
								this.props.availableMetricsValues.Priority.length
									? FilterElementType.simple
									: FilterElementType.disabled
							}
							value={this.state.currentMetricsValue.Priority}
							placeholder="Select"
							writable={false}
							dropDownValues={this.props.availableMetricsValues.Priority}
							onChange={this.changeDropdownValue("Priority")}
							onClear={this.clearDropdownValue("Priority")}
						/>
					</div>

					<div className="predict-text__dropdown predict-text__areas_of_testing">
						<span className="predict-text__dropdown-title">Area of Testing</span>
						<DropdownElement
							type={
								this.props.availableMetricsValues.areas_of_testing.length
									? FilterElementType.simple
									: FilterElementType.disabled
							}
							value={this.state.currentMetricsValue.areas_of_testing}
							placeholder="Select"
							writable={false}
							dropDownValues={this.props.availableMetricsValues.areas_of_testing}
							onChange={this.changeDropdownValue("areas_of_testing")}
							onClear={this.clearDropdownValue("areas_of_testing")}
						/>
					</div>
				</div>

				<div className="predict-text__buttons">
					<Button
						styled={ButtonStyled.Flat}
						className="predict-text__reset-all"
						iconSize={20}
						text="Clear All"
						icon={IconType.delete}
						onClick={this.clearAll}
						disabled={!this.state.text}
					/>

					<Button
						className="predict-text__predict"
						text="Predict"
						icon={IconType.check}
						type="submit"
						onClick={this.predict}
						disabled={!this.state.text}
						iconSize={28}
					/>
				</div>
			</div>
		);
	}
}

export default PredictText;
