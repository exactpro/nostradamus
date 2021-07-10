import React, { Component } from "react";
import PredictionsContainer from "app/modules/settings/parts/predictions/components/predictions-container/predictions-container";
import { connect, ConnectedProps } from "react-redux";
import { RootStore } from "app/common/types/store.types";
import { PredictionTableData } from "app/common/store/settings/types";
import SettingsLayout from "app/modules/settings/settings_layout/settings_layout";
import "app/modules/settings/parts/predictions/predictions.scss";
import { sendSettingsPredictionsData } from "app/common/store/settings/thunks";
import { deepCopyData } from "app/common/functions/helper";
import PredictionsForm from "app/modules/settings/parts/predictions/components/form/form";

interface State {
	predictions: PredictionTableData[];
	isSettingsDefault: boolean;
}

class SettingsPredictions extends Component<Props, State> {
	constructor(props: Props) {
		super(props);
		this.state = this.getDefaultObjectState();
	}

	// Get default state method
	getDefaultObjectState = () => {
		const predictions = deepCopyData<PredictionTableData[]>(
			this.props.defaultPredictions.predictions_table_settings
		);
		return {
			predictions,
			isSettingsDefault: true,
		};
	};

	// Component methods
	addPredictionBlock = (name: string) => {
		const { predictions } = this.state;
		const newPrediction: PredictionTableData = {
			name,
			is_default: false,
			position: predictions.length + 1,
			settings: 0,
		};
		this.setState({
			predictions: [...predictions, newPrediction],
			isSettingsDefault: false,
		});
	};

	deletePredictionBlock = (index: number) => () => {
		const { predictions } = this.state;
		predictions.splice(index, 1);

		this.setState({
			predictions: this.fixPredictionsBlocksOrder(predictions),
			isSettingsDefault: false,
		});
	};

	fixPredictionsBlocksOrder = (predictionsArr: PredictionTableData[]) => {
		return predictionsArr.map((item, index) => ({ ...item, position: index + 1 }));
	};

	changeValueBlocksOrder = (indexOfDraggedVal: number, indexOfNewPosition: number) => {
		const { predictions } = this.state;
		const val = predictions.splice(indexOfDraggedVal, 1)[0];
		predictions.splice(indexOfNewPosition, 0, val);

		this.setState({
			predictions: this.fixPredictionsBlocksOrder(predictions),
			isSettingsDefault: false,
		});
	};

	// Layout function: Save and Clear methods
	savePredictions = () => {
		const { predictions } = this.state;
		this.props.sendSettingsPredictionsData(predictions);
		this.setState({ isSettingsDefault: true });
	};

	setDefaultPredictions = () => {
		this.setState(this.getDefaultObjectState());
	};

	render() {
		const { predictions, isSettingsDefault } = this.state;

		const defaultNames = this.props.defaultPredictions.field_names;

		const excludeNames = predictions.map((item) => item.name);

		const allowedPredictionAdding =
			predictions.find((item: PredictionTableData) => !item.is_default) !== undefined;

		return (
			<SettingsLayout
				title="Predictions"
				cancelButtonDisable={isSettingsDefault}
				cancelButtonHandler={this.setDefaultPredictions}
				saveButtonDisable={isSettingsDefault}
				saveButtonHandler={this.savePredictions}
			>
				<div className="settings-predictions">
					<PredictionsForm
						names={defaultNames}
						excludeNames={excludeNames}
						allowedAdding={allowedPredictionAdding}
						onAddPredictionBlock={this.addPredictionBlock}
					/>

					<div className="settings-predictions__main">
						<PredictionsContainer
							values={predictions}
							onDeletePrediction={this.deletePredictionBlock}
							onChangePredictionsOrder={this.changeValueBlocksOrder}
						/>
					</div>
				</div>
			</SettingsLayout>
		);
	}
}

const mapStateToProps = (store: RootStore) => ({
	defaultPredictions: store.settings.settingsStore.defaultSettings.predictions_table,
});

const mapDispatchToProps = { sendSettingsPredictionsData };

const connector = connect(mapStateToProps, mapDispatchToProps);

type Props = ConnectedProps<typeof connector>;

export default connector(SettingsPredictions);
