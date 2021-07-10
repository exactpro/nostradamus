import React, { useState } from "react";
import { SettingsFilterData } from "app/modules/settings/parts/filter/filter";
import FilterTableRow from "app/modules/settings/parts/filter/components/table/table-row/table-row";
import { FilterElementType } from "app/modules/settings/elements/elements-types";
import "./table.scss";

interface Props {
	tableRows: SettingsFilterData[];
	names: string[];
	excludeNames: string[];
	onAcceptTableRowEditing: (index: number, rowData: SettingsFilterData) => void;
	onDeleteTableRow: (index: number) => void;
}

export default function FilterTable(props: Props) {
	// Table state
	const invalidName = "";
	const [editName, setEditName] = useState<string>(invalidName);

	// Table methods
	const getTableRowParityStatus = (index: number, name: string) => {
		if (name === editName) {
			return FilterElementType.edited;
		}
		if (index % 2 === 1) {
			return FilterElementType.odd;
		}
		return FilterElementType.even;
	};

	const editTableRowData = (name: string) => {
		return editName === invalidName ? () => setEditName(name) : undefined;
	};

	const acceptTableRowEditing = (index: number) => (rowData: SettingsFilterData) => {
		props.onAcceptTableRowEditing(index, rowData);
		setEditName(invalidName);
	};

	const deleteTableRow = (index: number) => () => {
		props.onDeleteTableRow(index);
	};

	return (
		<div className="settings-filter-table">
			{props.tableRows.map(({ name, type }, index) => (
				<FilterTableRow
					key={name}
					status={getTableRowParityStatus(index, name)}
					isAllowedEditing={editName !== invalidName}
					names={props.names}
					excludeNames={props.excludeNames}
					chosenName={name}
					chosenFiltrationType={type}
					onEditTableRowData={editTableRowData(name)}
					onAcceptTableRowEditing={acceptTableRowEditing(index)}
					onDeleteTableRow={deleteTableRow(index)}
				/>
			))}
		</div>
	);
}
