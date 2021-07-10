import React from "react";
import cn from "classnames";
import { ThunkDispatch } from "redux-thunk";
import { AnyAction } from "redux";
import Icon, { IconType, IconSize } from "app/common/components/icon/icon";
import DropdownElement from "app/common/components/native-components/dropdown-element/dropdown-element";
import { FilterElementType } from "app/modules/settings/elements/elements-types";
import { useDispatch, useSelector } from "react-redux";
import { RootStore } from "app/common/types/store.types";
import { TrainingSubSection } from "app/modules/settings/parts/training/store/types";
import {
	sendSettingsTrainingData,
	uploadSettingsTrainingSubfieldData,
} from "app/modules/settings/parts/training/store/thunks";
import "./source-field.scss";

interface Props {
	sourceField: string;
	isAllowedEditing: boolean;
	onModifySourceField: (sourceField: string) => void;
}

export default function SourceField(props: Props) {
	// Selector for extraction source_filed names from training store
	const sourceFieldNames = useSelector(
		(store: RootStore) => store.settings.settingsTrainingStore.source_field.source_field_names
	);

	// Function for thunk dispatching
	const dispatch: ThunkDispatch<void, void, AnyAction> = useDispatch();

	// Uploading chosen source_field
	const setMarkUpSource = async (source_field: string) => {
		setTimeout(() => {
			dispatch(sendSettingsTrainingData({ source_field }, TrainingSubSection.source_field)).then(
				() => {
					props.onModifySourceField(source_field);
					dispatch(uploadSettingsTrainingSubfieldData(TrainingSubSection.markup_entities));
				}
			);
		}, 1000);
	};

	return (
		<div className="settings-training-source">
			<p className="settings-training-source__title">Source Field</p>
			<DropdownElement
				type={FilterElementType.simple}
				value={props.sourceField}
				dropDownValues={sourceFieldNames}
				placeholder="Select or Enter"
				onChange={setMarkUpSource}
				onClear={() => props.onModifySourceField("")}
				style={{ width: "30%" }}
			/>

			{props.isAllowedEditing ? (
				<Icon type={IconType.check} className="settings-training-source__check" />
			) : (
				<Icon
					type={IconType.leftArrow}
					size={IconSize.big}
					className="settings-training-source__arrow-left"
				/>
			)}

			<span
				className={cn("settings-training-source__inscription", {
					"settings-training-source__inscription_success": props.isAllowedEditing,
				})}
			>
				{props.isAllowedEditing ? "Source Field Saved" : "Set Source Field first to add Entities"}
			</span>
		</div>
	);
}
