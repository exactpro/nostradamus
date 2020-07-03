import React, {Component} from "react";
import cn from "classnames";
import "app/modules/settings/fields/settings_filter/settings_filter.scss";
import InputElement from "app/modules/settings/elements/input-element/input-element";
import DropdownElement from "app/modules/settings/elements/dropdown-element/dropdown-element";
import {FilterElementType} from "app/modules/settings/elements/elements-types";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import Button, { ButtonStyled } from 'app/common/components/button/button';
import {connect, ConnectedProps} from "react-redux";
import {RootStore} from "app/common/types/store.types";
import {SettingsSections} from "app/common/store/settings/types";
import {sendSettings} from "app/common/store/settings/thunks";

interface SettingsFilterData{
  [key: string]: string,
  name: string,
  filtration_type: string,
}

interface SettingsFilterState{
  [key: string]: boolean|Array<SettingsFilterData>|SettingsFilterData|Array<FilterElementType>,
  settings: Array<SettingsFilterData>,
  dataInput: SettingsFilterData,
  dataEdit: SettingsFilterData,
  status: Array<FilterElementType>,
  isSettingsDefault: boolean,
}

interface SettingsFilterProps{
  section: SettingsSections.filters | SettingsSections.qaFilters,
}

class SettingsFilter extends Component<Props, SettingsFilterState>{

  constructor(props: Props)
  {
    super(props);
    this.state.settings=[...props.defaultSettings[props.section]];
    this.state.status=props.defaultSettings[props.section].map((_:any,index:number)=>index%2===1? FilterElementType.odd: FilterElementType.even);
  }

  state:SettingsFilterState={
    settings:[],
    dataInput:{
      name:"",
      filtration_type:"",
    },
    dataEdit:{
      name:"",
      filtration_type:"",
    },
    status:[],
    isSettingsDefault: true,
  }


  detectIsSettingsDefault = (isSettingsDefault: boolean = false) => this.setState({isSettingsDefault})

  setFieldData = (keyField: string = "dataInput", valField: string = "name") => (value: string) => {
    let data: SettingsFilterData = this.state[keyField] as SettingsFilterData;
    data[valField] = value;
    this.setState({
      [keyField]:data
    });
  }

  clearFieldData = (keyField: string = "dataInput", valField?: string) => () => {
    let data: SettingsFilterData = this.state[keyField] as SettingsFilterData;
    valField? data[valField] = "" : data={name:"", filtration_type: ""};
    this.setState({
      [keyField]:data,
    });
  }

  addPosition = () => {
    let {settings,status} = this.state;
    settings.push({...this.state.dataInput});
    status.push(status.length%2===1? FilterElementType.odd: FilterElementType.even);
    this.setState({
      settings,
      status,
    });
    this.clearFieldData("dataInput")();
    this.detectIsSettingsDefault();
  }

  changeHoverStatus = (index: number) => ({type}: any) => {
    let {status} = this.state;
    switch (type) {
      case "mouseenter":
        status[index] = FilterElementType.hovered;
        break;
      default:
        status[index] = index%2===1? FilterElementType.odd: FilterElementType.even;
        break;
    }
    this.setState({status});
  }

  editPosition = (index: number) => () => {
    let {status, dataEdit} = this.state;
    dataEdit = {...this.state.settings[index]};
    status[index] = FilterElementType.edited;
    this.setState({status, dataEdit});
  };

  acceptEditing = (index: number) => () => {
    let {settings,status} = this.state;
    settings[index]={...this.state.dataEdit};
    status[index] = index%2===1? FilterElementType.odd: FilterElementType.even;
    this.setState({
      settings,
      status,
    });
    this.clearFieldData("dataEdit");
    this.detectIsSettingsDefault();
  }

  deletePosition = (index: number) => () =>{
    let {settings, status} = this.state;
    settings.splice(index,1);
    status.pop();
    this.setState({
      settings,
      status,
    });
    this.detectIsSettingsDefault();
  }

  isButtonValid = (field: string = "dataInput") => {
    let data: SettingsFilterData = this.state[field] as SettingsFilterData;
    return !(data.name && data.filtration_type);
  }

  isHoverValid = (index: number) => this.state.status[index]!==FilterElementType.edited? this.changeHoverStatus(index): undefined;

  clearSettings = () => {
    this.setState({
      settings: [...this.props.defaultSettings[this.props.section]],
      status: this.props.defaultSettings[this.props.section].map((_:any,index:number)=>index%2===1? FilterElementType.odd: FilterElementType.even)
    });
    this.detectIsSettingsDefault(true);
  }

  saveSettings = () => {
    this.props.sendSettings(this.props.section, this.state.settings);
    this.detectIsSettingsDefault(true);
  }

  render(){
    return(
      <div className="settings-filter">
        <p className="settings-filter__title">Filter</p>

        <div className="settings-filter-header">

          <div className="settings-filter-name">
            <p className="settings-filter-header__title">Name</p>
            <InputElement onChange={this.setFieldData()}
                          onClear={this.clearFieldData("dataInput", "name")}
                          style={{width:"90%"}}
                          value={this.state.dataInput.name}/>
          </div>

          <div className="settings-filter-type">

            <p className="settings-filter-header__title">Filtration Type</p>
            <div className="settings-filter-header__dropdown-wrapper">
              <DropdownElement  onChange={this.setFieldData("dataInput", "filtration_type")}
                                onClear={this.clearFieldData("dataInput", "filtration_type")}
                                value={this.state.dataInput.filtration_type}/>

              <button className={cn("settings-filter-header__add-position", "settings-filter__button")}
                      onClick={this.addPosition}
                      disabled={this.isButtonValid()}>
                <Icon size={IconSize.small} type={IconType.close}/>
              </button>

            </div>

          </div>

        </div>

        <div className="settings-filter-main">
          {
            this.state.settings.map(({name,filtration_type},index)=>(
            <div  key={index}
                  className="settings-filter-main__section"
                  onMouseEnter={this.isHoverValid(index)}
                  onMouseLeave={this.isHoverValid(index)}>

              <div className={cn("settings-filter-name", "settings-filter-name_tabled")}>
                <InputElement type={this.state.status[index]}
                              value={this.state.status[index]===FilterElementType.edited? this.state.dataEdit.name: name}
                              onClear={this.clearFieldData("dataEdit", "name")}
                              onChange={this.setFieldData("dataEdit")}/>
              </div>

              <div className="settings-filter-type">
                <div className="settings-filter-type__dropdown-wrapper">
                  <DropdownElement  type={this.state.status[index] }
                                    value={this.state.status[index]===FilterElementType.edited? this.state.dataEdit.filtration_type: filtration_type}
                                    onChange={this.setFieldData("dataEdit","filtration_type")}
                                    onClear={this.clearFieldData("dataEdit", "filtration_type")}/>

                  {
                    this.state.status[index] === FilterElementType.edited &&
                    <button className={cn("settings-filter-type__accept-button", "settings-filter__button")}
                            onClick={this.acceptEditing(index)}
                            disabled={this.isButtonValid("dataEdit")}>
                      <Icon type={IconType.check} size={IconSize.normal}/>
                    </button>
                  }

                </div>
              </div>

              {
                this.state.status[index] === FilterElementType.hovered &&
                <div className="settings-filter-main__section-edit-wrapper">

                  <button className="settings-filter-main__edit-button"
                          onClick={this.editPosition(index)}
                          disabled={this.state.status.includes(FilterElementType.edited)}>
                    <Icon type={IconType.edit2} size={IconSize.normal}/>
                  </button>

                  <button className="settings-filter-main__delete-button"
                          onClick={this.deletePosition(index)}>
                    <Icon type={IconType.delete} size={IconSize.normal}/>
                  </button>

                </div>
              }

            </div>
          ))
        }
        </div>

        <div className="settings-filter-footer">
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
                  disabled={this.state.isSettingsDefault || !this.state.settings.length}/>
        </div>

      </div>
    )
  }
}

const mapStateToProps = ({settings}: RootStore) => ({
  defaultSettings: settings.defaultSettings
})

const mapDispatchToProps = {
  sendSettings,
}

const connector = connect(mapStateToProps, mapDispatchToProps)

type PropsFromRedux = ConnectedProps<typeof connector>;
type Props = PropsFromRedux & SettingsFilterProps;

export default connector(SettingsFilter)
