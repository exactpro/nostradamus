import React, {Component} from "react";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import Button, { ButtonStyled } from 'app/common/components/button/button';
import InputPredictionsElement from "app/modules/settings/elements/input-predictions-element/input-predictions-element";
import cn from "classnames";
import {connect, ConnectedProps} from "react-redux";
import {RootStore} from "app/common/types/store.types";
import {sendSettingsData} from "app/common/store/settings/thunks";
import {PredictionTableData, SettingsSections} from "app/common/store/settings/types";
import "app/modules/settings/fields/settings_predictions/settings_predictions.scss";
import DropdownElement from "../../elements/dropdown-element/dropdown-element";

interface SettingsPredictionsState{
  names: string[],
  predictions: PredictionTableData[],
  dataInput: string,
  isSettingsDefault: boolean,
}

class SettingsPredictions extends Component<SettingsPredictionsProps, SettingsPredictionsState>{

  constructor(props: SettingsPredictionsProps)
  {
    super(props);
    this.state = this.getDefaultStateObject();
  }

  detectIsSettingsDefault = (isSettingsDefault: boolean = false) => this.setState({isSettingsDefault})

  setInputData = (dataInput: string) => {
    this.setState({dataInput});
  }

  clearInputData = () => {
    this.setInputData("");
  }

  addPrediction = () => {
    let {predictions} = this.state;

    predictions.push({
      name: this.state.dataInput,
      is_default: false,
      position: predictions.length+1,
      settings: 0,
    });

    this.setState({predictions});
    this.clearInputData();
    this.detectIsSettingsDefault();
  }

  deletePrediction = (index: number) => () => {
    let {predictions} = this.state;

    predictions.splice(index, 1);

    this.setState({predictions});
    this.fixPredictionOrder();
  }

  editPrediction = (index: number, name: string) => {
    let {predictions} = this.state;

    predictions[index].name= name;

    this.setState({predictions});
  }

  fixPredictionOrder = () => {
    let predictions = this.state.predictions.map((item,index)=>({...item, position: index+1}));

    this.setState({predictions});
  }

  changePredictionsOrder = (indexOfDraggedVal: number, indexOfNewPosition: number) =>
  {
    let {predictions}=this.state;
    let val = predictions.splice(indexOfDraggedVal,1)[0];

    predictions.splice(indexOfNewPosition,0,val);

    this.setState({predictions});
    this.fixPredictionOrder();
    this.detectIsSettingsDefault();
  }

  saveSettings =() => {
    this.props.sendSettingsData(SettingsSections.predictions, this.state.predictions);

    this.detectIsSettingsDefault(true);
  }

  setDefaultSettings =() => {
    this.setState(this.getDefaultStateObject());
  }

  getDefaultStateObject = (): SettingsPredictionsState => ({
    names: [...this.props.predictions.field_names],
    predictions:[...this.props.predictions.predictions_table_settings],
    dataInput: "",
    isSettingsDefault: true,
  })

  render(){
    let excludeNames = this.state.predictions.map(item=>item.name);

    return (
      <div className="settings-predictions">
        <p className="settings-predictions__title">Predictions</p>

        <div className="settings-predictions-header">
          <p className="settings-predictions-header__title">Add Own Element</p>
          <div className="settings-predictions-header__wrapper">
            <DropdownElement value={this.state.dataInput}
                             onChange={this.setInputData}
                             onClear={this.clearInputData}
                             dropDownValues={this.state.names}
                             excludeValues={excludeNames}/>
            <button className={cn("settings-predictions__add-position", "settings-predictions__button")}
                    onClick={this.addPrediction}
                    disabled={!this.state.dataInput || this.state.predictions.find((item:PredictionTableData)=>!item.is_default) !== undefined}>
              <Icon size={IconSize.small} type={IconType.close}/>
            </button>
          </div>
        </div>

        <div className="settings-predictions-main">
          <InputPredictionsElement  values={this.state.predictions}
                                    onClear={this.deletePrediction}
                                    onChange={this.editPrediction}
                                    onChangeOrder={this.changePredictionsOrder}/>
        </div>

        <div className="settings-predictions-footer">
          <Button text="Cancel"
                  icon={IconType.close}
                  iconSize={IconSize.normal}
                  styled={ButtonStyled.Flat}
                  onClick={this.setDefaultSettings}
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
  predictions: settings.settingsStore.defaultSettings.predictions_table,
})

const mapDispatchToProps = {
  sendSettingsData,
}

const connector = connect(mapStateToProps, mapDispatchToProps)

type PropsFromRedux = ConnectedProps<typeof connector>;
type SettingsPredictionsProps = PropsFromRedux & {};

export default connector(SettingsPredictions);
