import React, {Component} from "react";
import "app/modules/settings/settings.scss";
import {RootStore} from "app/common/types/store.types";
import { IconType } from 'app/common/components/icon/icon';
import {activateSettings} from "app/common/store/settings/actions";
import {connect, ConnectedProps} from "react-redux";
import Button, { ButtonStyled } from 'app/common/components/button/button';
import AnalysisAndTrainingSection from 'app/modules/settings/sections/analysis-and-training-section/analysis-and-training-section';
import QAMetricsSection from 'app/modules/settings/sections/qa-metrics-section/qa-metrics-section';
import SlidingWindow from "app/common/components/sliding-window/sliding-window";

enum SettingsTab{
  analysisAndTraining = "Analysis & Training",
  QAMetrics = "QA Metrics",
}

interface State{
  activeTab: SettingsTab,
}

class Settings extends Component<Props, State> {

  state={
    activeTab: SettingsTab.analysisAndTraining,
  }

  selectTab = (tab: SettingsTab) => () => {
    this.setState({
      ...this.state,
      activeTab: tab,
    })
  }

  closeSettings = () => {
    this.props.activateSettings()
  }


  render(){
    return (
      <div className="settings-module">
        <SlidingWindow title="Settings"
                       isOpen={this.props.isOpen}
                       onClose={this.closeSettings}>
        {this.props.isOpen &&

          <div className="settings-block-wrapper">

              <div className="settings-block__button-wrapper">

                <Button className="settings-block__button"
                        text="Analysis & Training"
                        icon={IconType.analysis}
                        styled={ButtonStyled.Flat}
                        selected={this.state.activeTab === SettingsTab.analysisAndTraining}
                        disabled={this.state.activeTab === SettingsTab.analysisAndTraining}
                        onClick={this.selectTab(SettingsTab.analysisAndTraining)}/>

                <Button className="settings-block__button_shifted"
                        text="QA Metrics"
                        icon={IconType.QAMetrics}
                        styled={ButtonStyled.Flat}
                        selected={this.state.activeTab === SettingsTab.QAMetrics}
                        disabled={this.state.activeTab === SettingsTab.QAMetrics}
                        onClick={this.selectTab(SettingsTab.QAMetrics)}/>

              </div>

              {
                this.state.activeTab === SettingsTab.analysisAndTraining &&
                <AnalysisAndTrainingSection/>
              }

              {
                this.state.activeTab === SettingsTab.QAMetrics &&
                <QAMetricsSection/>
              }

          </div>}
        </SlidingWindow>
      </div>
    );
  }
}

const mapStateToProps = ({settings}: RootStore) =>({
  isOpen: settings.settingsStore.isOpen,
});

const mapDispatchToProps = {
  activateSettings,
};

const connector = connect(mapStateToProps, mapDispatchToProps)

type PropsFromRedux = ConnectedProps<typeof connector>;
type Props = PropsFromRedux & {};

export default connector(Settings)
