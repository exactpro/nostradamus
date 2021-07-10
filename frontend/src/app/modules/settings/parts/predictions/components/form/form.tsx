import React, { useState } from "react";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import DropdownElement from "app/common/components/native-components/dropdown-element/dropdown-element";
import "./form.scss";

interface Props {
	names: string[];
	excludeNames: string[];
	allowedAdding: boolean;

	onAddPredictionBlock: (prediction: string) => void;
}

export default function PredictionsForm(props: Props) {
	const [prediction, setPrediction] = useState<string>("");

	const addPredictionBlock = () => {
		props.onAddPredictionBlock(prediction);
		setPrediction("");
	};

	return (
		<div className="settings-predictions-form">
			<p className="settings-predictions-form__title">Add Own Element</p>
			<div className="settings-predictions-form__wrapper">
				<DropdownElement
					value={prediction}
					onChange={(value) => setPrediction(value)}
					onClear={() => setPrediction("")}
					dropDownValues={props.names}
					excludeValues={props.excludeNames}
				/>
				<button
					type="button"
					className="settings-predictions-form__add-position"
					onClick={addPredictionBlock}
					disabled={props.allowedAdding || !prediction}
				>
					<Icon size={IconSize.small} type={IconType.close} />
				</button>
			</div>
		</div>
	);
}
