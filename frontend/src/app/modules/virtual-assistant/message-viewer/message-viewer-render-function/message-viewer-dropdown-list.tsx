import React, { useState } from "react";
import SelectWindow from "app/common/components/native-components/select-window/select-window";
import Button, { ButtonStyled } from "app/common/components/button/button";
import cn from "classnames";

interface MessageViewerDropdownListProps {
	allDropdownValues: string[];
	sendDropdownListData: (item: string, renderItem?: string) => () => void;
}

export default function MessageViewerDropdownList(props: MessageViewerDropdownListProps) {
	const [dropdownListValues, setDropdownListValues] = useState<string[]>([]);

	const { allDropdownValues } = props;

	const selectDropdownListValue = (value: string, isChecked: boolean) => () => {
		if (isChecked) setDropdownListValues(dropdownListValues.filter((item) => item !== value));
		else setDropdownListValues([...dropdownListValues, value]);
	};

	const selectDropdownListData = () => {
		props.sendDropdownListData(JSON.stringify(dropdownListValues), dropdownListValues.join(", "))();
		setDropdownListValues([]);
	};

	return (
		<div className="message-viewer-dropdown-list">
			<SelectWindow
				selectWindowAllValues={allDropdownValues}
				selectWindowCheckedValues={dropdownListValues}
				searchable
				placeholder="Select a project"
				onSelectValue={selectDropdownListValue}
			>
				<div className="message-viewer-widget-buttons">
					<Button
						className={cn("message-viewer-widget-buttons__send", {
							"message-viewer-widget-buttons__send_disabled": !dropdownListValues.length,
						})}
						text="Send Selected"
						styled={ButtonStyled.Flat}
						type="submit"
						onClick={selectDropdownListData}
						disabled={!dropdownListValues.length}
					/>
				</div>
			</SelectWindow>
		</div>
	);
}
