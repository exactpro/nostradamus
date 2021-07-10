import React, { Component } from "react";
import "app/modules/settings/parts/filter/filter.scss";
import { connect, ConnectedProps } from "react-redux";
import { RootStore } from "app/common/types/store.types";
import { SettingsDataUnion, SettingsSections } from "app/common/store/settings/types";
import { caseInsensitiveStringCompare, deepCopyData } from "app/common/functions/helper";
import SettingsLayout from "app/modules/settings/settings_layout/settings_layout";
import FilterForm from "app/modules/settings/parts/filter/components/form/form";
import FilterTable from "app/modules/settings/parts/filter/components/table/table";

export interface SettingsFilterData {
	name: string;
	type: string;
}

interface SettingsFilterProps {
	section: SettingsSections.filters | SettingsSections.qaFilters;
	saveDataFunc: (data: SettingsDataUnion | any) => void;
}

interface State {
	filters: SettingsFilterData[];
	isSettingsDefault: boolean;
}

class SettingsFilter extends Component<Props, State> {
	constructor(props: Props) {
		super(props);
		this.state = this.getDefaultObjectState();
	}

	// Get default state method
	getDefaultObjectState = () => {
		const filters = deepCopyData(
			this.props.defaultSettings[this.props.section].filter_settings.sort((a, b) =>
				caseInsensitiveStringCompare(a.name, b.name)
			)
		);
		return {
			filters,
			isSettingsDefault: true,
		};
	};

	// Settings modification methods
	addTableRow = (filter: SettingsFilterData) => {
		const { filters } = this.state;
		this.setState({
			filters: [...filters, filter],
			isSettingsDefault: false,
		});
	};

	acceptTableRowEditing = (index: number, rowData: SettingsFilterData) => {
		const filters = [...this.state.filters];
		filters[index] = { ...rowData };
		this.setState({ filters, isSettingsDefault: false });
	};

	deleteTableRow = (index: number) => {
		const { filters } = this.state;
		filters.splice(index, 1);
		this.setState({ filters, isSettingsDefault: false });
	};

	// Layout function: Save and Clear methods
	setDefaultFilters = () => {
		this.setState(this.getDefaultObjectState());
	};

	saveFilters = () => {
		const { filters } = this.state;
		this.props.saveDataFunc(filters);
		this.setState({ isSettingsDefault: true });
	};

	render() {
		const { filters, isSettingsDefault } = this.state;

		const names = this.props.defaultSettings[this.props.section].names;
		const excludeNames = filters.map((item) => item.name);

		return (
			<SettingsLayout
				title="Filter"
				cancelButtonHandler={this.setDefaultFilters}
				cancelButtonDisable={isSettingsDefault}
				saveButtonHandler={this.saveFilters}
				saveButtonDisable={isSettingsDefault || !filters.length}
			>
				<div className="settings-filter">
					<FilterForm names={names} excludeNames={excludeNames} onAddTableRow={this.addTableRow} />

					<FilterTable
						tableRows={filters}
						names={names}
						excludeNames={excludeNames}
						onAcceptTableRowEditing={this.acceptTableRowEditing}
						onDeleteTableRow={this.deleteTableRow}
					/>
				</div>
			</SettingsLayout>
		);
	}
}

const mapStateToProps = (store: RootStore) => ({
	defaultSettings: store.settings.settingsStore.defaultSettings,
});

const connector = connect(mapStateToProps);

type Props = ConnectedProps<typeof connector> & SettingsFilterProps;

export default connector(SettingsFilter);
