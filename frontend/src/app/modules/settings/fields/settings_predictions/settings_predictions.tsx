import React, { Component } from "react";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import Button, { ButtonStyled } from "app/common/components/button/button";
import InputPredictionsElement from "app/modules/settings/elements/input-predictions-element/input-predictions-element";
import cn from "classnames";
import { connect, ConnectedProps } from "react-redux";
import { RootStore } from "app/common/types/store.types";
import { sendSettingsData } from "app/common/store/settings/thunks";
import { PredictionTableData, SettingsSections } from "app/common/store/settings/types";
import "app/modules/settings/fields/settings_predictions/settings_predictions.scss";
import DropdownElement from "app/common/components/native-components/dropdown-element/dropdown-element";

interface SettingsPredictionsState {
	names: string[];
	predictions: PredictionTableData[];
	dataInput: string;
	isSettingsDefault: boolean;
}

class SettingsPredictions extends Component<SettingsPredictionsProps, SettingsPredictionsState> {
	constructor(props: SettingsPredictionsProps) {
		super(props);
		this.state = this.getDefaultStateObject();
	}

	detectIsSettingsDefault = (isSettingsDefault = false) => this.setState({ isSettingsDefault });

	setInputData = (dataInput: string) => {
		this.setState({ dataInput });
	};

	clearInputData = () => {
		this.setInputData("");
	};

	addPredictionBlock = () => {
		const { predictions, dataInput } = this.state;

		predictions.push({
			name: dataInput,
			is_default: false,
			position: predictions.length + 1,
			settings: 0,
		});

		this.setState({ predictions });
		this.clearInputData();
		this.detectIsSettingsDefault();
	};

	deletePredictionBlock = (index: number) => () => {
		const { predictions } = this.state;

		predictions.splice(index, 1);

		this.setState({ predictions });
		this.fixPredictionsBlocksOrder();
		this.detectIsSettingsDefault();
	};

	fixPredictionsBlocksOrder = () => {
		let { predictions } = this.state;
		predictions = predictions.map((item, index) => ({ ...item, position: index + 1 }));
		this.setState({ predictions });
	};

	changeValueBlocksOrder = (indexOfDraggedVal: number, indexOfNewPosition: number) => {
		const { predictions } = this.state;
		const val = predictions.splice(indexOfDraggedVal, 1)[0];

		predictions.splice(indexOfNewPosition, 0, val);

		this.setState({ predictions });
		this.fixPredictionsBlocksOrder();
		this.detectIsSettingsDefault();
	};

	saveSettings = () => {
		const { sendSettingsData } = this.props;
		const { predictions } = this.state;
		// eslint-disable-next-line @typescript-eslint/no-floating-promises
		sendSettingsData(SettingsSections.predictions, predictions);

		this.detectIsSettingsDefault(true);
	};

	setDefaultSettings = () => {
		this.setState(this.getDefaultStateObject());
	};

	getDefaultStateObject = (): SettingsPredictionsState => {
		const { predictions } = this.props;

		return {
			names: [...predictions.field_names],
			predictions: [...predictions.predictions_table_settings],
			dataInput: "",
			isSettingsDefault: true,
		};
	};

	render() {
		const { predictions, dataInput, names, isSettingsDefault } = this.state;
		const excludeNames = predictions.map((item) => item.name);

		return (
			<div className="settings-predictions">
				<p className="settings-predictions__title">Predictions</p>

				<div className="settings-predictions-header">
					<p className="settings-predictions-header__title">Add Own Element</p>
					<div className="settings-predictions-header__wrapper">
						<DropdownElement
							value={dataInput}
							onChange={this.setInputData}
							onClear={this.clearInputData}
							dropDownValues={names}
							excludeValues={excludeNames}
						/>
						<button
							type="button"
							className={cn("settings-predictions__add-position", "settings-predictions__button")}
							onClick={this.addPredictionBlock}
							disabled={
								!dataInput ||
								predictions.find((item: PredictionTableData) => !item.is_default) !== undefined
							}
						>
							<Icon size={IconSize.small} type={IconType.close} />
						</button>
					</div>
				</div>

				<div className="settings-predictions-main">
					<InputPredictionsElement
						values={predictions}
						onDeletePrediction={this.deletePredictionBlock}
						onChangePredictionsOrder={this.changeValueBlocksOrder}
					/>
				</div>

				<div className="settings-predictions-footer">
					<Button
						text="Cancel"
						icon={IconType.close}
						iconSize={IconSize.normal}
						styled={ButtonStyled.Flat}
						onClick={this.setDefaultSettings}
						disabled={isSettingsDefault}
					/>
					<Button
						text="Save Changes"
						icon={IconType.check}
						iconSize={IconSize.normal}
						onClick={this.saveSettings}
						disabled={isSettingsDefault}
					/>
				</div>
			</div>
		);
	}
}

const mapStateToProps = ({ settings }: RootStore) => ({
	predictions: settings.settingsStore.defaultSettings.predictions_table,
});

const mapDispatchToProps = {
	sendSettingsData,
};

const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;
type SettingsPredictionsProps = PropsFromRedux & unknown;

export default connector(SettingsPredictions);
