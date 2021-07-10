import React from "react";
import DropdownElement from "app/common/components/native-components/dropdown-element/dropdown-element";
import { FilterElementType } from "app/modules/settings/elements/elements-types";
import InputElement from "app/modules/settings/elements/input-element/input-element";
import { BugResolutionElement } from "app/modules/settings/parts/training/store/types";
import { useSelector } from "react-redux";
import { RootStore } from "app/common/types/store.types";
import "./bug-resolution.scss";

interface BugResolutionProps {
	isAllowedEditing: boolean;
	bugResolution: BugResolutionElement[];

	onModifyBugResolution: (bugResolution: BugResolutionElement[]) => void;
}

export default function BugResolution(props: BugResolutionProps) {
	// Selector for extraction bug_resolution_names from training store
	const bugResolutionNames = useSelector(
		(store: RootStore) => store.settings.settingsTrainingStore.bug_resolution.resolution_names
	);

	const changeResolutionValue = (index: number) => (value: string) => {
		const resolutionArr = props.bugResolution;
		resolutionArr[index].value = value;
		props.onModifyBugResolution([...resolutionArr]);
	};

	return (
		<div className="settings-training-bug-resolution">
			<BugResolutionRow
				bugResolution={props.bugResolution[0]}
				names={bugResolutionNames}
				isAllowedEditing={props.isAllowedEditing}
				excludeValue={props.bugResolution[1].value}
				onChangeBugResolutionValue={changeResolutionValue(0)}
			/>
			<BugResolutionRow
				bugResolution={props.bugResolution[1]}
				names={bugResolutionNames}
				isAllowedEditing={props.isAllowedEditing}
				excludeValue={props.bugResolution[0].value}
				onChangeBugResolutionValue={changeResolutionValue(1)}
			/>
		</div>
	);
}

interface BugResolutionRowProps {
	bugResolution: BugResolutionElement;
	names: string[];
	isAllowedEditing: boolean;
	excludeValue: string;
	onChangeBugResolutionValue: (value: string) => void;
}

// Section of bug resolution table
function BugResolutionRow(props: BugResolutionRowProps) {
	return (
		<div className="settings-training-bug-resolution-row">
			<div className="settings-training-bug-resolution-row__metric">
				<p className="settings-training-bug-resolution-row__metric-title">Metric</p>
				<InputElement type={FilterElementType.disabled} placeholder={props.bugResolution.metric} />
			</div>
			<div className="settings-training-bug-resolution-row__value">
				<p className="settings-training-bug-resolution-row__value-title">Value</p>
				<DropdownElement
					placeholder="Value"
					type={props.isAllowedEditing ? FilterElementType.simple : FilterElementType.disabled}
					dropDownValues={props.names}
					excludeValues={[props.excludeValue]}
					value={props.bugResolution.value}
					onChange={props.onChangeBugResolutionValue}
					onClear={() => props.onChangeBugResolutionValue("")}
				/>
			</div>
		</div>
	);
}
