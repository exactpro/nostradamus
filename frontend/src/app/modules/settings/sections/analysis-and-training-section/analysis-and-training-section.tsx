import React, {Component} from "react";
import CircleSpinner from 'app/common/components/circle-spinner/circle-spinner';
import SettingsFilter from "app/modules/settings/fields/settings_filter/setings_filter";
import SettingsTraining from "app/modules/settings/fields/settings_training/settings_training"
import "app/modules/settings/sections/analysis-and-training-section/analysis-and-training-section.scss";
import {SettingsSections} from "app/common/store/settings/types";
import {uploadSettings} from "app/common/store/settings/thunks";
import {connect, ConnectedProps} from "react-redux";
import {RootStore} from "app/common/types/store.types";
import { HttpStatus } from 'app/common/types/http.types';

class AnalysisAndTrainingSection extends Component<Props>{

  componentDidMount = () => {
    this.props.uploadSettings(SettingsSections.filters)
    this.props.uploadSettings(SettingsSections.training)
  }
  render(){
    return(
      <div className="analysis-and-training-section">
        {
          this.props.status[SettingsSections.filters] === HttpStatus.FINISHED &&
          <div className="analysis-and-training-section__filter">
            <SettingsFilter section={SettingsSections.filters}/>
          </div>
        }
        {
          this.props.status[SettingsSections.filters] === HttpStatus.RELOADING &&
          <div className="analysis-and-training-section__spinner">
            <CircleSpinner alignCenter/>
          </div>
        }
        {
          this.props.status[SettingsSections.training] === HttpStatus.FINISHED &&
          <div className="analysis-and-training-section__training">
            <SettingsTraining/>
          </div>
        }
        {
          this.props.status[SettingsSections.training] === HttpStatus.RELOADING &&
          <div className="analysis-and-training-section__spinner">
            <CircleSpinner alignCenter/>
          </div>
        }
      </div>
    )
  }
}
const mapStateToProps = ({settings}: RootStore) => ({
  status: settings.status,
})

const mapDispatchToProps = {
  uploadSettings,
}


const connector = connect(mapStateToProps, mapDispatchToProps)

type PropsFromRedux = ConnectedProps<typeof connector>;
type Props = PropsFromRedux & {};

export default connector(AnalysisAndTrainingSection)
