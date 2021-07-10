import React, { Component } from "react";
import { connect, ConnectedProps } from "react-redux";
import { RootStore } from "app/common/types/store.types";
import { sendSettingsTrainingData } from "app/modules/settings/parts/training/store/thunks";
import {
	MarkUpEntitiesElement,
	BugResolutionElement,
} from "app/modules/settings/parts/training/store/types";
import SettingsLayout from "app/modules/settings/settings_layout/settings_layout";
import { deepCopyData } from "app/common/functions/helper";
import SourceField from "./components/source-field/source-field";
import BugResolution from "./components/bug-resolution/bug-resolution";
import MarkUpEntities from "./components/mark-up-entities/mark-up-entities";
import "./training.scss";

interface State {
	sourceField: string;
	markupEntities: MarkUpEntitiesElement[];
	bugResolution: BugResolutionElement[];
	isSettingsDefault: boolean;
}

class SettingsTraining extends Component<Props, State> {
	constructor(props: Props) {
		super(props);
		this.state = this.getDefaultObjectState();
	}

	// Get default state method
	getDefaultObjectState = () => {
		const sourceField = this.props.settingsFromRedux.source_field.source_field;
		const markupEntities = deepCopyData(
			this.props.settingsFromRedux.markup_entities.mark_up_entities
		);

		const bugResolution = deepCopyData(
			this.props.settingsFromRedux.bug_resolution.resolution_settings
		);
		while (bugResolution.length < 2) {
			bugResolution.push({ metric: "Resolution", value: "" });
		}

		return {
			sourceField,
			markupEntities,
			bugResolution,
			isSettingsDefault: true,
		};
	};

	// Methods wrappers for state modification
	modifySourceField = (sourceField: string) => {
		this.setState({
			sourceField,
		});
	};

	modifyBugResolution = (bugResolution: BugResolutionElement[]) => {
		this.setState({
			bugResolution,
			isSettingsDefault: false,
		});
	};

	modifyMarkUpEntities = (markupEntities: MarkUpEntitiesElement[]) => {
		this.setState({
			markupEntities,
			isSettingsDefault: false,
		});
	};

	// Layout methods
	saveTraining = () => {
		const data = {
			mark_up_entities: this.state.markupEntities,
			bug_resolution: this.state.bugResolution,
		};

		this.props.sendSettingsTrainingData(data);
		this.setState({ isSettingsDefault: true });
	};

	setDefaultTraining = () => {
		this.setState({ ...this.getDefaultObjectState() });
	};

	render() {
		const { isSettingsDefault, sourceField, markupEntities, bugResolution } = this.state;

		// Check if each field - source_field, markup_entities and bug_resolution were filled
		const isSaveButtonDisabled = !(
			!isSettingsDefault &&
			sourceField.length &&
			markupEntities.length &&
			bugResolution.length &&
			bugResolution[0].value.length &&
			bugResolution[1].value.length
		);

		return (
			<SettingsLayout
				title="Training"
				cancelButtonDisable={isSettingsDefault}
				cancelButtonHandler={this.setDefaultTraining}
				saveButtonDisable={isSaveButtonDisabled}
				saveButtonHandler={this.saveTraining}
			>
				<div className="settings-training">
					<p className="settings-training__subtitle">Areas of Testing</p>

					<SourceField
						sourceField={sourceField}
						isAllowedEditing={!!sourceField}
						onModifySourceField={this.modifySourceField}
					/>

					<MarkUpEntities
						markUpEntities={markupEntities}
						isAllowedEditing={!!sourceField}
						onModifyMarkUpEntities={this.modifyMarkUpEntities}
					/>

					<p className="settings-training__subtitle">Bug Resolution</p>

					<BugResolution
						isAllowedEditing={!!sourceField}
						bugResolution={bugResolution}
						onModifyBugResolution={this.modifyBugResolution}
					/>
				</div>
			</SettingsLayout>
		);
	}
}

const mapStateToProps = (store: RootStore) => ({
	settingsFromRedux: store.settings.settingsTrainingStore,
});

const mapDispatchToProps = { sendSettingsTrainingData };

const connector = connect(mapStateToProps, mapDispatchToProps);

type Props = ConnectedProps<typeof connector>;

export default connector(SettingsTraining);
