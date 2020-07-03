import React, {Component} from "react";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import Button, { ButtonStyled } from 'app/common/components/button/button';
import InputElement from "app/modules/settings/elements/input-element/input-element";
import InputPredictionsElement from "app/modules/settings/elements/input-predictions-element/input-predictions-element";
import cn from "classnames";
import {connect, ConnectedProps} from "react-redux";
import {RootStore} from "app/common/types/store.types";
import {sendSettings} from "app/common/store/settings/thunks";
import {PredictionTableType, SettingsSections} from "app/common/store/settings/types";
import "app/modules/settings/fields/settings_predictions/settings_predictions.scss";

interface SettingsPredictionsState{
  values: PredictionTableType[],
  dataInput: string,
  isSettingsDefault: boolean,
}

class SettingsPredictions extends Component<SettingsPredictionsProps, SettingsPredictionsState>{

  state: SettingsPredictionsState = {
    values:[],
    dataInput: "",
    isSettingsDefault: true,
  }

  constructor(props: SettingsPredictionsProps)
  {
    super(props);
    this.state.values=[...this.props.predictions];
  }

  detectIsSettingsDefault = (isSettingsDefault: boolean = false) => this.setState({isSettingsDefault})

  setInputData = (value: string) => {
    this.setState({dataInput: value});
  }

  clearInputData = () => {
    this.setState({dataInput:""});
  }

  addPosition = () => {
    let {values} = this.state;
    values.push({
      name: this.state.dataInput,
      is_default: false,
      position: values.length+1,
    });
    this.setState({values});
    this.clearInputData();
    this.detectIsSettingsDefault();
  }

  clearValue = (index: number) => () => {
    let {values} = this.state;
    values.splice(index, 1);
    this.setState({values});
    this.repairOrder();
  }

  changeValue = (index: number, name: string) => {
    let {values} = this.state;
    values[index].name= name;
    this.setState({values});
  }

  repairOrder = () => {
    let values = this.state.values.map((item,index)=>({...item, position: index+1}));
    this.setState({values});
  }

  changeValuesOrder = (indexOfDraggedVal: number, indexOfNewPosition: number) =>
  {
    let {values}=this.state;
    let val = values.splice(indexOfDraggedVal,1)[0];
    values.splice(indexOfNewPosition,0,val);
    this.setState({values});
    this.repairOrder();
    this.detectIsSettingsDefault();
  }

  saveSettings =() => {
    this.props.sendSettings(SettingsSections.predictions, this.state.values);
    this.detectIsSettingsDefault(true);
  }

  clearSettings =() => {
    this.setState({
      values:[...this.props.predictions],
      dataInput: "",
    });
    this.detectIsSettingsDefault(true);
  }

  render(){
    return (
      <div className="settings-predictions">
        <p className="settings-predictions__title">Predictions</p>

        <div className="settings-predictions-header">
          <p className="settings-predictions-header__title">Add Own Element</p>
          <div className="settings-predictions-header__wrapper">
            <InputElement value={this.state.dataInput}
                          onChange={this.setInputData}
                          onClear={this.clearInputData}
                          placeholder="Element"/>
            <button className={cn("settings-predictions__add-position", "settings-predictions__button")}
                    onClick={this.addPosition}
                    disabled={!this.state.dataInput || this.state.values.length>=7}>
              <Icon size={IconSize.small} type={IconType.close}/>
            </button>
          </div>
        </div>

        <div className="settings-predictions-main">
          <InputPredictionsElement  values={this.state.values}
                                    onClear={this.clearValue}
                                    onChange={this.changeValue}
                                    onChangeOrder={this.changeValuesOrder}/>
        </div>

        <div className="settings-predictions-footer">
          <Button text="Cancel"
                  icon={IconType.close}
                  iconSize={IconSize.normal}
                  styled={ButtonStyled.Flat}
                  onClick={this.clearSettings}
                  disabled={this.state.isSettingsDefault}/>
          <Button text="Save Changes"
                  icon={IconType.check}
                  iconSize={IconSize.normal}
                  onClick={this.saveSettings}
                  disabled={this.state.isSettingsDefault}/>
        </div>

      </div>
    )
  }
}

const mapStateToProps = ({settings}: RootStore) => ({
  predictions: settings.defaultSettings.predictions_table,
})

const mapDispatchToProps = {
  sendSettings,
}

const connector = connect(mapStateToProps, mapDispatchToProps)

type PropsFromRedux = ConnectedProps<typeof connector>;
type SettingsPredictionsProps = PropsFromRedux & {};

export default connector(SettingsPredictions);
