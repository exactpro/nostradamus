import BacklightTextArea from 'app/common/components/backlight-textarea/backlight-text-area';
import Button, { ButtonStyled } from 'app/common/components/button/button';
import Icon, { IconType } from 'app/common/components/icon/icon';
import React from 'react';
import cn from 'classnames';

import './predict-text.scss';

export interface Keywords {
	Priority: string[],
	resolution: string[],
	areas_of_testing: string[]
}

export interface PredictMetric {
	metric: PredictMetricsName,
	value: string
}

export type PredictMetricsName = 'Priority' | 'resolution' | 'areas_of_testing';

interface State {
	text: string,
	currentMetricsValue: {
		[key in PredictMetricsName]: string | undefined
	}
}

interface Props {
	availableMetricsValues: Keywords,
	keywords?: Keywords,
	onChangePredictOption: (predictOption: PredictMetric) => void
	onPredict: (text: string) => void,
	onClearAll: () => void,
}

class PredictText extends React.Component<Props, State> {

	state = {
		text: '',
		currentMetricsValue: {
			Priority: undefined,
			resolution: undefined,
			areas_of_testing: undefined,
		},
	};

	onChangeText = (text: string) => {
		this.setState({
			text,
			currentMetricsValue: {
				Priority: undefined,
				resolution: undefined,
				areas_of_testing: undefined,
			},
		});
		this.props.onClearAll();
	};

	predict = () => {
		this.props.onPredict(this.state.text);
	};

	clearAll = () => {
		this.setState({
			text: '',
			currentMetricsValue: {
				Priority: undefined,
				resolution: undefined,
				areas_of_testing: undefined,
			},
		});

		this.props.onClearAll();
	}

	changeDropdownValue = (option: PredictMetricsName) => (e: React.ChangeEvent<HTMLSelectElement>) => {
		this.props.onChangePredictOption({
			metric: option,
			value: e.target.value,
		});

		this.setState({
			currentMetricsValue: {
				...this.state.currentMetricsValue,
				[option]: e.target.value || undefined,
			},
		});
	};

	render() {

		return (
			<div className="predict-text">
				<BacklightTextArea
					text={this.state.text}
					onChangeText={this.onChangeText}
					keywords={this.props.keywords}
				/>

				<div className="predict-text__dropdowns-wrapper">

					<label className="predict-text__dropdown" htmlFor="resolution">
						Resolution
						<select
							className={cn('predict-text__select', { 'predict-text__select_color_red': this.state.currentMetricsValue.resolution })}
							name="resolution"
							id="resolution"
							disabled={!this.props.availableMetricsValues.resolution.length || !this.state.text}
							value={this.state.currentMetricsValue.resolution}
							onChange={this.changeDropdownValue('resolution')}
						>
							<option value="">Select</option>
							{
								this.props.availableMetricsValues.resolution.map((option) => (
									<option key={option} value={option}>{option}</option>
								))
							}
						</select>

						<Icon size={16} type={IconType.down} className="predict-text__select-icon" />
					</label>

					<label className="predict-text__dropdown" htmlFor="priority">
						Priority
						<select
							className={cn('predict-text__select', { 'predict-text__select_color_yellow': this.state.currentMetricsValue.Priority })}
							name="priority"
							id="priority"
							disabled={!this.props.availableMetricsValues.Priority.length || !this.state.text}
							value={this.state.currentMetricsValue.Priority}
							onChange={this.changeDropdownValue('Priority')}
						>
							<option value="">Select</option>
							{
								this.props.availableMetricsValues.Priority.map((option) => (
									<option key={option} value={option}>{option}</option>
								))
							}
						</select>

						<Icon size={16} type={IconType.down} className="predict-text__select-icon" />
					</label>

					<label className="predict-text__dropdown" htmlFor="areas_of_testing">
						Area of Testing
						<select
							className={cn('predict-text__select', { 'predict-text__select_color_purple': this.state.currentMetricsValue.areas_of_testing })}
							name="areas_of_testing"
							id="areas_of_testing"
							disabled={!this.props.availableMetricsValues.areas_of_testing.length || !this.state.text}
							value={this.state.currentMetricsValue.areas_of_testing}
							onChange={this.changeDropdownValue('areas_of_testing')}
						>
							<option value="">Select</option>
							{
								this.props.availableMetricsValues.areas_of_testing.map((option) => (
									<option key={option} value={option}>{option}</option>
								))
							}
						</select>

						<Icon size={16} type={IconType.down} className="predict-text__select-icon" />
					</label>

				</div>

				<div className="predict-text__buttons">
					<Button
						styled={ButtonStyled.Flat}
						className="predict-text__reset-all"
						iconSize={20}
						text="Clear All" icon={IconType.delete}
						onClick={this.clearAll}
						disabled={!this.state.text}
					/>

					<Button
						className="predict-text__predict"
						text="Predict" icon={IconType.check}
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
