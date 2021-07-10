import React, { useState } from "react";
import cn from "classnames";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import DropdownElement from "app/common/components/native-components/dropdown-element/dropdown-element";
import { FilterDropdownType } from "app/modules/settings/elements/elements-types";
import { SettingsFilterData } from "app/modules/settings/parts/filter/filter";
import "./form.scss";

interface Props {
	names: string[];
	excludeNames: string[];
	onAddTableRow: (rowData: SettingsFilterData) => void;
}

export default function SettingsFilterForm(props: Props) {
	// Form state
	const [name, setName] = useState<string>("");
	const [type, setFiltrationType] = useState<string>("");

	// Form method
	const addTableRow = () => {
		props.onAddTableRow({ name, type });
		setName("");
		setFiltrationType("");
	};

	return (
		<div className="settings-filter-form">
			<div className="settings-filter-form__name">
				<p className="settings-filter-form__title">Name</p>
				<DropdownElement
					onChange={(value) => setName(value)}
					onClear={() => setName("")}
					style={{ width: "90%" }}
					value={name}
					dropDownValues={props.names}
					excludeValues={props.excludeNames}
				/>
			</div>

			<div className="settings-filter-form__type">
				<p className="settings-filter-form__title">Filtration Type</p>
				<div className="settings-filter-form__dropdown-wrapper">
					<DropdownElement
						onChange={(value) => setFiltrationType(value)}
						onClear={() => setFiltrationType("")}
						value={type}
						dropDownValues={Object.values(FilterDropdownType)}
						writable={false}
					/>

					<button
						className={cn("settings-filter-form__add-position", "settings-filter__button")}
						onClick={addTableRow}
						type="button"
						disabled={!(name && type)}
					>
						<Icon size={IconSize.small} type={IconType.close} />
					</button>
				</div>
			</div>
		</div>
	);
}
