import React, { useEffect, useState } from "react";
import cn from "classnames";
import Icon, { IconType, IconSize } from "app/common/components/icon/icon";
import DropdownElement from "app/common/components/native-components/dropdown-element/dropdown-element";
import {
	FilterElementType,
	FilterDropdownType,
} from "app/modules/settings/elements/elements-types";
import { SettingsFilterData } from "app/modules/settings/parts/filter/filter";
import "./table-row.scss";

interface Props {
	status: FilterElementType;
	chosenName: string;
	chosenFiltrationType: string;
	isAllowedEditing: boolean;
	names: string[];
	excludeNames: string[];

	onDeleteTableRow: () => void;
	onEditTableRowData?: () => void;
	onAcceptTableRowEditing: (rowData: SettingsFilterData) => void;
}

export default function FilterTableRow(props: Props) {
	// Table row state data
	const [name, setName] = useState<string>(props.chosenName);
	const [type, setFiltrationType] = useState<string>(props.chosenFiltrationType);
	const [tableRowStatus, setTableRowStatus] = useState<FilterElementType>(props.status);

	// Table row methods
	const changeHoverStatus = (isHovered = true) => () => {
		if (props.status === FilterElementType.edited) {
			return;
		}

		if (isHovered) {
			tableRowStatus !== FilterElementType.hovered && setTableRowStatus(FilterElementType.hovered);
		} else {
			setTableRowStatus(props.status);
		}
	};

	const acceptRowEditing = () => {
		props.onAcceptTableRowEditing({
			name,
			type,
		});
	};

	// Effect hook for renew state data with props change
	useEffect(() => {
		setTableRowStatus(props.status);
		setFiltrationType(props.chosenFiltrationType);
		setName(props.chosenName);
	}, [props.status, props.chosenFiltrationType, props.chosenName]);

	return (
		<div
			className="settings-filter-table-row"
			onMouseLeave={changeHoverStatus(false)}
			onMouseMove={changeHoverStatus()}
		>
			<div className={cn("settings-filter-table-row__name", "settings-filter-table-row__tabled")}>
				<DropdownElement
					type={tableRowStatus === FilterElementType.hovered ? tableRowStatus : props.status}
					value={name}
					onChange={(value) => setName(value)}
					onClear={() => setName("")}
					dropDownValues={props.names}
					excludeValues={props.excludeNames.filter((exName) => exName !== props.chosenName)}
				/>
			</div>

			<div className="settings-filter-table-row__type">
				<div className="settings-filter-table-row__dropdown-wrapper">
					<DropdownElement
						type={tableRowStatus === FilterElementType.hovered ? tableRowStatus : props.status}
						value={type}
						onChange={(value) => setFiltrationType(value)}
						onClear={() => setFiltrationType("")}
						dropDownValues={Object.values(FilterDropdownType)}
						writable={false}
					/>

					{tableRowStatus === FilterElementType.edited && (
						<button
							type="button"
							className="settings-filter-table-row__accept-button"
							onClick={acceptRowEditing}
							disabled={!(type && name)}
						>
							<Icon type={IconType.check} size={IconSize.normal} />
						</button>
					)}
				</div>
			</div>

			{tableRowStatus === FilterElementType.hovered && (
				<div className="settings-filter-table-row__section-edit-wrapper">
					<button
						type="button"
						className="settings-filter-table-row__edit-button"
						onClick={props.onEditTableRowData}
						disabled={props.isAllowedEditing}
					>
						<Icon type={IconType.edit2} size={IconSize.normal} />
					</button>

					<button
						type="button"
						className="settings-filter-table-row__delete-button"
						onClick={props.onDeleteTableRow}
					>
						<Icon type={IconType.delete} size={IconSize.normal} />
					</button>
				</div>
			)}
		</div>
	);
}
