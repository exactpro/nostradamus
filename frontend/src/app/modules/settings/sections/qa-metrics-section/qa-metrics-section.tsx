import React, {Component} from "react";
import {SettingsSections} from "app/common/store/settings/types";
import {uploadSettingsData} from "app/common/store/settings/thunks";
import {connect, ConnectedProps} from "react-redux";
import {RootStore} from "app/common/types/store.types";
import { HttpStatus } from 'app/common/types/http.types';
import CircleSpinner from 'app/common/components/circle-spinner/circle-spinner';
import SettingsFilter from "app/modules/settings/fields/settings_filter/setings_filter";
import SettingsPredictions from "app/modules/settings/fields/settings_predictions/settings_predictions"
import "app/modules/settings/sections/qa-metrics-section/qa-metrics-section.scss";

class QAMetricsSection extends Component<Props>{

  componentDidMount = () => {
    this.props.uploadSettingsData(SettingsSections.qaFilters)
    this.props.uploadSettingsData(SettingsSections.predictions)
  }

  render(){
    return(
      <div className="qa-metrics-section">
      {
        this.props.status[SettingsSections.predictions] === HttpStatus.FINISHED &&
        <div className="qa-metrics-section__predictions">
          <SettingsPredictions/>
        </div>
      }
      {
        this.props.status[SettingsSections.predictions] === HttpStatus.RELOADING &&
        <div className="qa-metrics-section__spinner">
          <CircleSpinner alignCenter/>
        </div>
      }
      {
        this.props.status[SettingsSections.qaFilters] === HttpStatus.FINISHED &&
        <div className="qa-metrics-section__filter">
          <SettingsFilter section={SettingsSections.qaFilters}/>
        </div>
      }
      {
        this.props.status[SettingsSections.qaFilters] === HttpStatus.RELOADING &&
        <div className="qa-metrics-section__spinner">
          <CircleSpinner alignCenter/>
        </div>
      }
      </div>
    )
  }
}

const mapStateToProps = ({settings}: RootStore) => ({
  status: settings.settingsStore.status,
})

const mapDispatchToProps = { uploadSettingsData }


const connector = connect(mapStateToProps, mapDispatchToProps)

type PropsFromRedux = ConnectedProps<typeof connector>;
type Props = PropsFromRedux & {};

export default connector(QAMetricsSection)
