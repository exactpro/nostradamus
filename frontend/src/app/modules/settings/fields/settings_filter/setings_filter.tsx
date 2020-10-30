import React, { Component } from "react";
import cn from "classnames";
import "app/modules/settings/fields/settings_filter/settings_filter.scss";
import DropdownElement from "app/common/components/native-components/dropdown-element/dropdown-element";
import {
	FilterElementType,
	FilterDropdownType,
} from "app/modules/settings/elements/elements-types";
import Icon, { IconSize, IconType } from "app/common/components/icon/icon";
import Button, { ButtonStyled } from "app/common/components/button/button";
import { connect, ConnectedProps } from "react-redux";
import { RootStore } from "app/common/types/store.types";
import { SettingsSections } from "app/common/store/settings/types";
import { sendSettingsData } from "app/common/store/settings/thunks";
import { caseInsensitiveStringCompare } from "app/common/functions/helper";

interface SettingsFilterData {
	[key: string]: string;
	name: string;
	filtration_type: string;
}

interface SettingsFilterState {
	[key: string]:
		| boolean
		| Array<SettingsFilterData>
		| SettingsFilterData
		| Array<FilterElementType>
		| string[];
	names: string[];
	settings: Array<SettingsFilterData>;
	dataInput: SettingsFilterData;
	dataEdit: SettingsFilterData;
	status: Array<FilterElementType>;
	isSettingsDefault: boolean;
}

interface SettingsFilterProps {
	section: SettingsSections.filters | SettingsSections.qaFilters;
}

class SettingsFilter extends Component<Props, SettingsFilterState> {
	constructor(props: Props) {
		super(props);
		this.state = this.getDefaultStateObject();
	}

	setFieldData = (keyField: "dataInput" | "dataEdit", valField: keyof SettingsFilterData) => (
		value: string
	) => {
		this.setState((prevState) => {
			const data: SettingsFilterData = prevState[keyField];
			data[valField] = value;
			return {
				[keyField]: data,
			};
		});
	};

	clearFieldData = (
		keyField: "dataInput" | "dataEdit",
		valField?: keyof SettingsFilterData
	) => () => {
		this.setState((prevState) => {
			let data: SettingsFilterData = prevState[keyField];

			if (valField) data[valField] = "";
			else data = { name: "", filtration_type: "" };

			return {
				[keyField]: data,
			};
		});
	};

	addTableRow = () => {
		const { settings, status, dataInput } = this.state;

		settings.push({ ...dataInput });
		status.push(this.getTableRowParity(status.length));

		this.setState({
			settings,
			status,
		});
		this.clearFieldData("dataInput")();
		this.detectIsSettingsDefault();
	};

	changeTableRowHoverStatus = (index: number) => ({ type }: any) => {
		const { status } = this.state;

		if (status[index] === FilterElementType.edited) return;

		switch (type) {
			case "mouseenter":
				status[index] = FilterElementType.hovered;
				break;
			default:
				status[index] = this.getTableRowParity(index);
				break;
		}

		this.setState({ status });
	};

	editTableRowData = (index: number) => () => {
		const { status, settings } = this.state;
		const dataEdit = { ...settings[index] };

		status[index] = FilterElementType.edited;

		this.setState({ status, dataEdit });
	};

	acceptTableRowEditing = (index: number) => () => {
		const { settings, status, dataEdit } = this.state;

		settings[index] = { ...dataEdit };
		status[index] = this.getTableRowParity(index);

		this.setState({
			settings,
			status,
		});
		this.detectIsSettingsDefault();
	};

	deleteTableRow = (index: number) => () => {
		const { settings, status } = this.state;
		settings.splice(index, 1);
		status.pop();
		this.setState({
			settings,
			status,
		});
		this.detectIsSettingsDefault();
	};

	setDefaultSettings = () => {
		this.setState(this.getDefaultStateObject());
	};

	saveSettings = () => {
		const { sendSettingsData, section } = this.props;
		const { settings } = this.state;
		// eslint-disable-next-line @typescript-eslint/no-floating-promises
		sendSettingsData(section, settings);
		this.detectIsSettingsDefault(true);
	};

	getDefaultStateObject = (): SettingsFilterState => {
		const { defaultSettings, section } = this.props;

		return {
			names: [...defaultSettings[section].names],
			settings: this.sortTableRows(defaultSettings[section].filter_settings),
			status: this.getDefaultTableRowsStatuses(defaultSettings[section].filter_settings.length),
			dataInput: {
				name: "",
				filtration_type: "",
			},
			dataEdit: {
				name: "",
				filtration_type: "",
			},
			isSettingsDefault: true,
		};
	};

	getDefaultTableRowsStatuses = (length: number) =>
		[...new Array<number>(length)].map((_, index) => this.getTableRowParity(index));

	sortTableRows = (arr: Array<SettingsFilterData>) =>
		[...arr].sort((firstItem: SettingsFilterData, secondItem: SettingsFilterData) =>
			caseInsensitiveStringCompare(firstItem.name, secondItem.name)
		);

	getTableRowParity = (numb: number) =>
		numb % 2 === 1 ? FilterElementType.odd : FilterElementType.even;

	detectIsSettingsDefault = (isSettingsDefault = false) => this.setState({ isSettingsDefault });

	isPositionAcceptButtonValid = (field: "dataInput" | "dataEdit") => {
		// eslint-disable-next-line react/destructuring-assignment
		const data: SettingsFilterData = this.state[field];
		return !(data.name && data.filtration_type);
	};

	render() {
		const { settings, dataInput, names, status, dataEdit, isSettingsDefault } = this.state;
		const excludeNames = settings.map((item) => item.name);

		return (
			<div className="settings-filter">
				<p className="settings-filter__title">Filter</p>

				<div className="settings-filter-header">
					<div className="settings-filter-name">
						<p className="settings-filter-header__title">Name</p>
						<DropdownElement
							onChange={this.setFieldData("dataInput", "name")}
							onClear={this.clearFieldData("dataInput", "name")}
							style={{ width: "90%" }}
							value={dataInput.name}
							dropDownValues={names}
							excludeValues={excludeNames}
						/>
					</div>

					<div className="settings-filter-type">
						<p className="settings-filter-header__title">Filtration Type</p>
						<div className="settings-filter-header__dropdown-wrapper">
							<DropdownElement
								onChange={this.setFieldData("dataInput", "filtration_type")}
								onClear={this.clearFieldData("dataInput", "filtration_type")}
								value={dataInput.filtration_type}
								dropDownValues={Object.values(FilterDropdownType)}
								writable={false}
							/>

							<button
								className={cn("settings-filter-header__add-position", "settings-filter__button")}
								onClick={this.addTableRow}
								type="button"
								disabled={this.isPositionAcceptButtonValid("dataInput")}
							>
								<Icon size={IconSize.small} type={IconType.close} />
							</button>
						</div>
					</div>
				</div>

				<div className="settings-filter-main">
					{settings.map(({ name, filtration_type }, index) => (
						<div
							key={name}
							className="settings-filter-main__section"
							onMouseEnter={this.changeTableRowHoverStatus(index)}
							onMouseLeave={this.changeTableRowHoverStatus(index)}
						>
							<div className={cn("settings-filter-name", "settings-filter-name_tabled")}>
								<DropdownElement
									type={status[index]}
									value={status[index] === FilterElementType.edited ? dataEdit.name : name}
									onClear={this.clearFieldData("dataEdit", "name")}
									onChange={this.setFieldData("dataEdit", "name")}
									dropDownValues={names}
									excludeValues={excludeNames.filter((exName) => exName !== name)}
								/>
							</div>

							<div className="settings-filter-type">
								<div className="settings-filter-type__dropdown-wrapper">
									<DropdownElement
										type={status[index]}
										value={
											status[index] === FilterElementType.edited
												? dataEdit.filtration_type
												: filtration_type
										}
										onChange={this.setFieldData("dataEdit", "filtration_type")}
										onClear={this.clearFieldData("dataEdit", "filtration_type")}
										dropDownValues={Object.values(FilterDropdownType)}
										writable={false}
									/>

									{status[index] === FilterElementType.edited && (
										<button
											type="button"
											className={cn(
												"settings-filter-type__accept-button",
												"settings-filter__button"
											)}
											onClick={this.acceptTableRowEditing(index)}
											disabled={this.isPositionAcceptButtonValid("dataEdit")}
										>
											<Icon type={IconType.check} size={IconSize.normal} />
										</button>
									)}
								</div>
							</div>

							{status[index] === FilterElementType.hovered && (
								<div className="settings-filter-main__section-edit-wrapper">
									<button
										type="button"
										className="settings-filter-main__edit-button"
										onClick={this.editTableRowData(index)}
										disabled={status.includes(FilterElementType.edited)}
									>
										<Icon type={IconType.edit2} size={IconSize.normal} />
									</button>

									<button
										type="button"
										className="settings-filter-main__delete-button"
										onClick={this.deleteTableRow(index)}
									>
										<Icon type={IconType.delete} size={IconSize.normal} />
									</button>
								</div>
							)}
						</div>
					))}
				</div>

				<div className="settings-filter-footer">
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
						disabled={isSettingsDefault || !settings.length}
					/>
				</div>
			</div>
		);
	}
}

const mapStateToProps = ({ settings }: RootStore) => ({
	defaultSettings: settings.settingsStore.defaultSettings,
});

const mapDispatchToProps = {
	sendSettingsData,
};

const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;
type Props = PropsFromRedux & SettingsFilterProps;

export default connector(SettingsFilter);
