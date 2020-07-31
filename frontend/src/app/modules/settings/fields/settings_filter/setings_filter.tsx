import React, {Component} from "react";
import cn from "classnames";
import "app/modules/settings/fields/settings_filter/settings_filter.scss"; 
import DropdownElement from "app/modules/settings/elements/dropdown-element/dropdown-element";
import {FilterElementType, FilterDropdownType} from "app/modules/settings/elements/elements-types";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import Button, { ButtonStyled } from 'app/common/components/button/button';
import {connect, ConnectedProps} from "react-redux";
import {RootStore} from "app/common/types/store.types";
import {SettingsSections} from "app/common/store/settings/types";
import {sendSettingsData} from "app/common/store/settings/thunks";

interface SettingsFilterData{
  [key: string]: string,
  name: string,
  filtration_type: string,
}

interface SettingsFilterState{
  [key: string]: boolean|Array<SettingsFilterData>|SettingsFilterData|Array<FilterElementType>| string[],
  names: string[], 
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
    this.state = this.getDefaultStateObject();
  }

  setFieldData = (keyField: "dataInput" | "dataEdit", valField: keyof SettingsFilterData) => (value: string) => {
    let data: SettingsFilterData = this.state[keyField];

    data[valField] = value;

    this.setState({
      [keyField]:data
    });
  }

  clearFieldData = (keyField: "dataInput" | "dataEdit", valField?: keyof SettingsFilterData) => () => {
    let data: SettingsFilterData = this.state[keyField];

    valField? data[valField] = "" : data={name:"", filtration_type: ""};

    this.setState({
      [keyField]:data,
    });
  }

  addTableRow = () => {
    let {settings,status} = this.state;

    settings.push({...this.state.dataInput});
    status.push(this.getTableRowParity(status.length));

    this.setState({
      settings,
      status,
    });
    this.clearFieldData("dataInput")();
    this.detectIsSettingsDefault();
  }

  changeTableRowHoverStatus = (index: number) => ({type}: any) => {
    let {status} = this.state;

    if(status[index]===FilterElementType.edited) return;

    switch (type) {
      case "mouseenter":
        status[index] = FilterElementType.hovered;
        break;
      default:
        status[index] = this.getTableRowParity(index);
        break;
    }

    this.setState({status});
  }

<<<<<<< HEAD
  editTableRowData = (index: number) => () => {
=======
  editPosition = (index: number) => () => {
>>>>>>> [Settings][Filter] Refactoring
    let {status} = this.state, dataEdit = {...this.state.settings[index]};

    status[index] = FilterElementType.edited;

    this.setState({status, dataEdit});
  };

<<<<<<< HEAD
  acceptTableRowEditing = (index: number) => () => {
=======
  acceptPositionEditing = (index: number) => () => {
>>>>>>> [Settings][Filter] Refactoring
    let {settings,status} = this.state;

    settings[index]={...this.state.dataEdit};
    status[index] = this.getTableRowParity(index);

    this.setState({
      settings,
      status,
    });
    this.detectIsSettingsDefault();
  }

  deleteTableRow = (index: number) => () =>{
    let {settings, status} = this.state;
    settings.splice(index,1);
    status.pop();
    this.setState({
      settings,
      status,
    });
    this.detectIsSettingsDefault();
  }

<<<<<<< HEAD
  setDefaultSettings = () => {
    this.setState(this.getDefaultStateObject());
  }

  saveSettings = () => {
    this.props.sendSettingsData(this.props.section, this.state.settings);
    this.detectIsSettingsDefault(true);
=======
  clearSettings = () => {
    this.setState(this.getDefaultStateObject());
>>>>>>> [Settings][Filter] Refactoring
  }

  getDefaultStateObject = (): SettingsFilterState => ({
      names: [...this.props.defaultSettings[this.props.section].names],
      settings: [...this.props.defaultSettings[this.props.section].filter_settings].sort((firstItem: SettingsFilterData, secondItem: SettingsFilterData)=>firstItem.name.toLowerCase().localeCompare(secondItem.name.toLowerCase())),
      status: this.props.defaultSettings[this.props.section].filter_settings.map((_:any,index:number)=>this.getTableRowParity(index)),
      dataInput: {
        name:"",
        filtration_type:"",
      },
      dataEdit:{
        name:"",
        filtration_type:"",
      },
      isSettingsDefault: true,
    })

  getTableRowParity = (numb: number) => numb%2===1? FilterElementType.odd: FilterElementType.even;

  detectIsSettingsDefault = (isSettingsDefault: boolean = false) => this.setState({isSettingsDefault});

  isPositionAcceptButtonValid = (field: "dataInput" | "dataEdit") => {
    let data: SettingsFilterData = this.state[field];
    return !(data.name && data.filtration_type);
  }

  getDefaultStateObject = (): SettingsFilterState => ({
      names: [...this.props.defaultSettings[this.props.section].names],
      settings: [...this.props.defaultSettings[this.props.section].filter_settings].sort((firstItem: SettingsFilterData, secondItem: SettingsFilterData)=>firstItem.name.toLowerCase().localeCompare(secondItem.name.toLowerCase())),
      status: this.props.defaultSettings[this.props.section].filter_settings.map((_:any,index:number)=>this.getTableRowParity(index)),
      dataInput: {
        name:"",
        filtration_type:"",
      },
      dataEdit:{
        name:"",
        filtration_type:"",
      },
      isSettingsDefault: true,
    })

  getTableRowParity = (numb: number) => numb%2===1? FilterElementType.odd: FilterElementType.even;

  detectIsSettingsDefault = (isSettingsDefault: boolean = false) => this.setState({isSettingsDefault});

  isPositionAcceptButtonValid = (field: "dataInput" | "dataEdit") => {
    let data: SettingsFilterData = this.state[field];
    return !(data.name && data.filtration_type);
  }

  getDefaultStateObject = (): SettingsFilterState => ({
      settings: [...this.props.defaultSettings[this.props.section]],
      status: this.props.defaultSettings[this.props.section].map((_:any,index:number)=>this.getTableRowParity(index)),
      dataInput: {
        name:"",
        filtration_type:"",
      },
      dataEdit:{
        name:"",
        filtration_type:"",
      },
      isSettingsDefault: true,
    })

  getTableRowParity = (numb: number) => numb%2===1? FilterElementType.odd: FilterElementType.even;

  detectIsSettingsDefault = (isSettingsDefault: boolean = false) => this.setState({isSettingsDefault});

  isPositionAcceptButtonValid = (field: "dataInput" | "dataEdit") => {
    let data: SettingsFilterData = this.state[field];
    return !(data.name && data.filtration_type);
  }

  render(){
    let excludeNames = this.state.settings.map(item=>item.name);

    return(
      <div className="settings-filter">
        <p className="settings-filter__title">Filter</p>

        <div className="settings-filter-header">

          <div className="settings-filter-name">
            <p className="settings-filter-header__title">Name</p>
<<<<<<< HEAD
            <DropdownElement onChange={this.setFieldData("dataInput", "name")}
                             onClear={this.clearFieldData("dataInput", "name")}
                             style={{width:"90%"}}
                             value={this.state.dataInput.name}
                             dropDownValues={this.state.names}
                             excludeValues={excludeNames}/>
=======
            <InputElement onChange={this.setFieldData("dataInput", "name")}
                          onClear={this.clearFieldData("dataInput", "name")}
                          style={{width:"90%"}}
                          value={this.state.dataInput.name}/>
>>>>>>> [Settings][Filter] Refactoring
          </div>

          <div className="settings-filter-type">

            <p className="settings-filter-header__title">Filtration Type</p>
            <div className="settings-filter-header__dropdown-wrapper">
              <DropdownElement  onChange={this.setFieldData("dataInput", "filtration_type")}
                                onClear={this.clearFieldData("dataInput", "filtration_type")}
                                value={this.state.dataInput.filtration_type}
                                dropDownValues={Object.values(FilterDropdownType)}
                                writable={false}/>

              <button className={cn("settings-filter-header__add-position", "settings-filter__button")}
<<<<<<< HEAD
                      onClick={this.addTableRow}
=======
                      onClick={this.addPosition}
>>>>>>> [Settings][Filter] Refactoring
                      disabled={this.isPositionAcceptButtonValid("dataInput")}>
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
<<<<<<< HEAD
                  onMouseEnter={this.changeTableRowHoverStatus(index)}
                  onMouseLeave={this.changeTableRowHoverStatus(index)}>

              <div className={cn("settings-filter-name", "settings-filter-name_tabled")}>
                <DropdownElement type={this.state.status[index]}
                                 value={this.state.status[index]===FilterElementType.edited? this.state.dataEdit.name: name}
                                 onClear={this.clearFieldData("dataEdit", "name")}
                                 onChange={this.setFieldData("dataEdit", "name")}
                                 dropDownValues={this.state.names}
                                 excludeValues={excludeNames.filter(exName=>exName!==name)}/>
=======
                  onMouseEnter={this.changeHoverStatus(index)}
                  onMouseLeave={this.changeHoverStatus(index)}>

              <div className={cn("settings-filter-name", "settings-filter-name_tabled")}>
                <InputElement type={this.state.status[index]}
                              value={this.state.status[index]===FilterElementType.edited? this.state.dataEdit.name: name}
                              onClear={this.clearFieldData("dataEdit", "name")}
                              onChange={this.setFieldData("dataEdit", "name")}/>
>>>>>>> [Settings][Filter] Refactoring
              </div>

              <div className="settings-filter-type">
                <div className="settings-filter-type__dropdown-wrapper">
                  <DropdownElement  type={this.state.status[index] }
                                    value={this.state.status[index]===FilterElementType.edited? this.state.dataEdit.filtration_type: filtration_type}
                                    onChange={this.setFieldData("dataEdit","filtration_type")}
                                    onClear={this.clearFieldData("dataEdit", "filtration_type")}
                                    dropDownValues={Object.values(FilterDropdownType)}
                                    writable={false}/>

                  {
                    this.state.status[index] === FilterElementType.edited &&
                    <button className={cn("settings-filter-type__accept-button", "settings-filter__button")}
<<<<<<< HEAD
                            onClick={this.acceptTableRowEditing(index)}
=======
                            onClick={this.acceptPositionEditing(index)}
>>>>>>> [Settings][Filter] Refactoring
                            disabled={this.isPositionAcceptButtonValid("dataEdit")}>
                      <Icon type={IconType.check} size={IconSize.normal}/>
                    </button>
                  }

                </div>
              </div>

              {
                this.state.status[index] === FilterElementType.hovered &&
                <div className="settings-filter-main__section-edit-wrapper">

                  <button className="settings-filter-main__edit-button"
                          onClick={this.editTableRowData(index)}
                          disabled={this.state.status.includes(FilterElementType.edited)}>
                    <Icon type={IconType.edit2} size={IconSize.normal}/>
                  </button>

                  <button className="settings-filter-main__delete-button"
                          onClick={this.deleteTableRow(index)}>
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
                  onClick={this.setDefaultSettings}
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
  defaultSettings: settings.settingsStore.defaultSettings
})

const mapDispatchToProps = {
  sendSettingsData,
}

const connector = connect(mapStateToProps, mapDispatchToProps)

type PropsFromRedux = ConnectedProps<typeof connector>;
type Props = PropsFromRedux & SettingsFilterProps;

export default connector(SettingsFilter)
