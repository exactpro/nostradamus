import React, { Component } from "react";
import { SettingsSections } from "app/common/store/settings/types";
import {
	uploadSettingsQAMetricsFilterData,
	uploadSettingsPredictionsData,
	sendSettingsQAMetricsFiltersData,
} from "app/common/store/settings/thunks";
import { connect, ConnectedProps } from "react-redux";
import { RootStore } from "app/common/types/store.types";
import { HttpStatus } from "app/common/types/http.types";
import CircleSpinner from "app/common/components/circle-spinner/circle-spinner";
import SettingsFilter from "app/modules/settings/parts/filter/filter";
import SettingsPredictions from "app/modules/settings/parts/predictions/predictions";
import "app/modules/settings/sections/qa-metrics-section/qa-metrics-section.scss";

class QAMetricsSection extends Component<Props> {
	componentDidMount = () => {
		const { uploadSettingsQAMetricsFilterData, uploadSettingsPredictionsData } = this.props;
		// eslint-disable-next-line @typescript-eslint/no-floating-promises
		uploadSettingsQAMetricsFilterData();
		// eslint-disable-next-line @typescript-eslint/no-floating-promises
		uploadSettingsPredictionsData();
	};

	render() {
		const { status, sendSettingsQAMetricsFiltersData } = this.props;

		return (
			<div className="qa-metrics-section">
				{status[SettingsSections.predictions] === HttpStatus.FINISHED && (
					<div className="qa-metrics-section__predictions">
						<SettingsPredictions />
					</div>
				)}
				{status[SettingsSections.predictions] === HttpStatus.RELOADING && (
					<div className="qa-metrics-section__spinner">
						<CircleSpinner alignCenter />
					</div>
				)}
				{status[SettingsSections.qaFilters] === HttpStatus.FINISHED && (
					<div className="qa-metrics-section__filter">
						<SettingsFilter
							section={SettingsSections.qaFilters}
							saveDataFunc={sendSettingsQAMetricsFiltersData}
						/>
					</div>
				)}
				{status[SettingsSections.qaFilters] === HttpStatus.RELOADING && (
					<div className="qa-metrics-section__spinner">
						<CircleSpinner alignCenter />
					</div>
				)}
			</div>
		);
	}
}

const mapStateToProps = ({ settings }: RootStore) => ({
	status: settings.settingsStore.status,
});

const mapDispatchToProps = {
	uploadSettingsQAMetricsFilterData,
	uploadSettingsPredictionsData,
	sendSettingsQAMetricsFiltersData,
};

const connector = connect(mapStateToProps, mapDispatchToProps);

type PropsFromRedux = ConnectedProps<typeof connector>;
type Props = PropsFromRedux & unknown;

export default connector(QAMetricsSection);
