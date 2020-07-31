import React, {Component} from "react";
import "app/modules/settings/fields/settings_training/settings_training.scss";
import InputElement from "app/modules/settings/elements/input-element/input-element";
import InputTrainingElement from "app/modules/settings/elements/input-training-element/input-training-element";
import {FilterElementType} from "app/modules/settings/elements/elements-types";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import Button, { ButtonStyled } from 'app/common/components/button/button';
import {MarkUpEntities, SettingsSections} from "app/common/store/settings/types";
import {connect, ConnectedProps} from "react-redux";
import {RootStore} from "app/common/types/store.types";
import {sendSettingsData} from "app/common/store/settings/thunks";
import {sendSettingsTrainingData} from "app/modules/settings/fields/settings_training/store/thunks";
import cn from "classnames";
import { MarkUpEntitiesData, BugResolutionData, SourceFieldData, MarkUpEntitiesElement, TrainingSubSection } from "app/modules/settings/fields/settings_training/store/types";
import DropdownElement from "app/modules/settings/elements/dropdown-element/dropdown-element";
import {uploadSettingsTrainingSubfieldData} from "app/modules/settings/fields/settings_training/store/thunks";

interface SettingsTrainingState{
  [key: string]: any,
  source_field: SourceFieldData,
  markup_entities: MarkUpEntitiesData,
  bug_resolution: BugResolutionData,
  markUpEntitiesInputData: MarkUpEntitiesElement,
  markUpEntitiesEditData: MarkUpEntitiesElement,
  status: FilterElementType[],
  isSettingsDefault: boolean,
  isAllowedEntitiesEditing: boolean,
}

class SettingsTraining extends Component<Props, SettingsTrainingState>{

  constructor(props: Props)
  {
    super(props);
    this.state=this.getDefaultStateObject();
  }

  setMarkUpEntitiesData = (keyField: "markUpEntitiesInputData" | "markUpEntitiesEditData", valField: keyof MarkUpEntities) => (value: string) => {
    let data: MarkUpEntitiesElement = this.state[keyField];
    if(valField==="area_of_testing") data.area_of_testing = value;
    else data.entities.push(value);
    this.setState({[keyField]: data});
  }

  clearMarkUpEntitiesInputData = (keyField: "markUpEntitiesInputData" | "markUpEntitiesEditData") => () => this.setMarkUpEntitiesData(keyField, "area_of_testing")("")

  clearMarkUpEntitiesBlockValueData = (keyField: "markUpEntitiesInputData" | "markUpEntitiesEditData") => (index: number) => {
    let data = this.state[keyField];
    data.entities.splice(index,1);
    this.setState({[keyField]:data});
  }
  

  setSourceFieldData = (name: string, isAllowedEntitiesEditing: boolean = false) => {
    let {source_field} = this.state;
    source_field.source_field=name;
    this.setState({source_field, isAllowedEntitiesEditing}); 
    this.detectIsSettingsDefault();
  } 

  setMarkUpSource = (name: string) => {
    this.setSourceFieldData(name);
    setTimeout(()=>this.props.sendSettingsTrainingData({source_field:name}, TrainingSubSection.source_field)
                  .then(isAllowedEntitiesEditing=>{
                    if(isAllowedEntitiesEditing) {
                      this.setState({isAllowedEntitiesEditing});
                      this.props.uploadSettingsTrainingSubfieldData(TrainingSubSection.markup_entities).then(markup_entities=> markup_entities? this.setState({markup_entities}): this.setState({isAllowedEntitiesEditing:false}))
                    }
                  
                  }),1000); 
  }

  setMarkUpSource = (name: string) => {
    this.setSourceFieldData(name);
    setTimeout(()=>this.props.sendTrainingData({source_field:name}, TrainingSubSection.source_field)
                  .then(isAllowedEntitiesEditing=>{
                    if(isAllowedEntitiesEditing) {
                      this.setState({isAllowedEntitiesEditing});
                      this.props.getTrainingDataSubField(TrainingSubSection.markup_entities).then(markup_entities=> markup_entities? this.setState({markup_entities}): this.setState({isAllowedEntitiesEditing:false}))
                    }
                  
                  }),1000); 
  }

  clearMarkUpSource = () => {
    this.setSourceFieldData("");
  }

  changeBugResolutionValue = (index: number) => (value: string) => {
    let {bug_resolution} = this.state;

    bug_resolution.resolution_settings[index]={
      metric: bug_resolution.resolution_settings[index].metric,
      value:value
    };

    this.setState({bug_resolution});
    this.detectIsSettingsDefault();
  }

  clearBugResolutionValue = (index: number) => () => {
    this.changeBugResolutionValue(index)("");
  }

  changeTableRowHoverStatus = (index: number) => ({type}: any) => {
    let {status} = this.state
    if(status[index]===FilterElementType.edited || !this.state.isAllowedEntitiesEditing) return

    switch (type) {
      case "mouseenter":
        status[index] = FilterElementType.hovered;
        break;
      default:
        status[index] = this.getTableRowParity(index);
        break;
    }

    this.setState({status})
  }

  addTableRow = () => {
    let {markup_entities, markUpEntitiesInputData, status} = this.state;
    markup_entities.mark_up_entities.push({...markUpEntitiesInputData});
    markUpEntitiesInputData={
      area_of_testing:"",
      entities:[],
    };
    status.push(this.getTableRowParity(markup_entities.mark_up_entities.length+1));

    this.setState({
      markup_entities,
      markUpEntitiesInputData,
      status,
    });
    this.detectIsSettingsDefault();
  } 

  editTableRowData = (index: number) => () => {
    let {status, markUpEntitiesEditData} = this.state;

    status[index]=FilterElementType.edited;
    markUpEntitiesEditData.area_of_testing = this.state.markup_entities.mark_up_entities[index].area_of_testing;
    markUpEntitiesEditData.entities = [...this.state.markup_entities.mark_up_entities[index].entities];

    this.setState({status, markUpEntitiesEditData});
  }

  acceptTableRowEditing = (index: number) => () => {
    let {status, markUpEntitiesEditData, markup_entities} = this.state

    status[index] = this.getTableRowParity(index);
    markup_entities.mark_up_entities[index]= markUpEntitiesEditData;
    markUpEntitiesEditData={
      area_of_testing:"",
      entities:[],
    };

    this.setState({
      status,
      markup_entities,
      markUpEntitiesEditData,
    });
    this.detectIsSettingsDefault();
  }

  deleteTableRow = (index: number) => () => {
    let {markup_entities, status} = this.state;

    markup_entities.mark_up_entities.splice(index,1);
    status.pop();

    this.setState({
      markup_entities,
      status});
    this.detectIsSettingsDefault();
  }

  saveSettings = () => {
    let settings = { 
      mark_up_entities:[...this.state.markup_entities.mark_up_entities],
      bug_resolution:[...this.state.bug_resolution.resolution_settings]
    };

    this.props.sendSettingsData(
      SettingsSections.training,
      settings);
    this.detectIsSettingsDefault(true);
  }

  setDefaultSettings = () => {
    let newState = this.getDefaultStateObject();
    this.setState({...newState}); 
  }

  detectIsSettingsDefault = (isSettingsDefault: boolean = false) => this.setState({isSettingsDefault})


  getTableRowParity = (index: number) => index%2===1? FilterElementType.odd: FilterElementType.even


  getDefaultStateObject = () => {
    let resolution_settings = ([{metric: "Resolution", value:""}, {metric: "Resolution", value:""}]).map((item: any, index: number) => this.props.training.bug_resolution.resolution_settings[index]? {...this.props.training.bug_resolution.resolution_settings[index]}: item)
    let bug_resolution = {...this.props.training.bug_resolution};
    bug_resolution.resolution_settings = resolution_settings; 

    return {
      source_field: {...this.props.training.source_field},
      markup_entities: {...this.props.training.markup_entities},
      bug_resolution: bug_resolution,
      markUpEntitiesInputData:{
        area_of_testing:"",
        entities:[]
      },
      markUpEntitiesEditData:{
        area_of_testing:"",
        entities:[]
      },
      status: this.props.training.markup_entities.mark_up_entities.map((_:any,index:number)=>this.getTableRowParity(index)),
      isSettingsDefault: true,
      isAllowedEntitiesEditing: !!this.props.training.source_field.source_field.length,
    }
}

  render(){ 
    let bugResolutionExcludeValues = this.state.bug_resolution.resolution_settings? this.state.bug_resolution.resolution_settings.map(item=>item.value): [];
    
    return(
      <div className="settings-training">
        <p className="settings-training__title">Training</p>

        <p className="settings-training__subtitle">Areas of Testing</p>

        <div className="settings-training-source">
          <p className="settings-training-source__title">Source Field</p>
          <DropdownElement type={FilterElementType.simple}
                           value={this.state.source_field.source_field}
                           dropDownValues={this.state.source_field.source_field_names} 
                           placeholder="Select or Enter"
                           onChange={this.setMarkUpSource}
                           onClear={this.clearMarkUpSource}
                           style={{width:"30%"}}/>

          { this.state.isAllowedEntitiesEditing? 
              <Icon type={IconType.check} className="settings-training-source__check"/>: 
              <span className="settings-training-source__arrow-left">&larr;</span>}
        
          <span className={cn("settings-training-source__inscription",{"settings-training-source__inscription_success": this.state.isAllowedEntitiesEditing})}>
            { this.state.isAllowedEntitiesEditing? <>Source Field Saved</>: <>Set Source Field first to add Entities</>}
          </span>
        
        </div>
        

        
        <div className="settings-training-table-header">

          <div className="settings-training-table-header__wrapper">
            <div className="settings-training-table-input">
              <p className="settings-training-table-header__field-title">Name</p>
              <InputElement type={this.state.isAllowedEntitiesEditing? FilterElementType.simple: FilterElementType.disabled}
                            value={this.state.markUpEntitiesInputData.area_of_testing}
                            placeholder="Name"
                            onChange={this.setMarkUpEntitiesData("markUpEntitiesInputData" ,"area_of_testing")}
                            onClear={this.clearMarkUpEntitiesInputData("markUpEntitiesInputData")}
                            style={{width:"90%"}}/>
            </div>

            <div className="settings-training-table-select">
              <p className="settings-training-table-header__field-title">Entities</p>
              <div className="settings-training-table-select__select-wrapper">
                <InputTrainingElement type={this.state.isAllowedEntitiesEditing? FilterElementType.simple: FilterElementType.disabled}
                                      onChange={this.setMarkUpEntitiesData("markUpEntitiesInputData", "entities")}
                                      onClear={this.clearMarkUpEntitiesBlockValueData("markUpEntitiesInputData")}
                                      dropDownValues={this.state.markup_entities.entity_names}
                                      values={this.state.markUpEntitiesInputData.entities}/>
                <button className={cn("settings-training__add-position", "settings-training__button")}
                        onClick={this.addTableRow}
                        disabled={!(this.state.markUpEntitiesInputData.area_of_testing && this.state.markUpEntitiesInputData.entities.length)}>
                  <Icon size={IconSize.small} type={IconType.close}/>
                </button>
              </div>
            </div>
          </div>

        </div>

        

        <div className="settings-training-table-main">
          {this.state.markup_entities.mark_up_entities.map((item:any,index: number)=>(
          <div  key={index} className="settings-training-table-main-section"
                onMouseEnter={this.changeTableRowHoverStatus(index)}
                onMouseLeave={this.changeTableRowHoverStatus(index)}>
            <div className={cn("settings-training-table-input","settings-training-table-input_tabled")}>
              <InputElement value={this.state.status[index]===FilterElementType.edited? this.state.markUpEntitiesEditData.area_of_testing:item.area_of_testing}
                            onChange={this.setMarkUpEntitiesData("markUpEntitiesEditData" ,"area_of_testing")}
                            onClear={this.clearMarkUpEntitiesInputData("markUpEntitiesEditData")}
                            type={this.state.status[index]}/>
            </div>
            <div className={cn("settings-training-table-select", "settings-training-table-main-section_select")}>
              <InputTrainingElement type={this.state.status[index]}
                                    onChange={this.setMarkUpEntitiesData("markUpEntitiesEditData" ,"entities")}
                                    onClear={this.clearMarkUpEntitiesBlockValueData("markUpEntitiesEditData")}
                                    dropDownValues={this.state.markup_entities.entity_names}
                                    values={this.state.status[index]===FilterElementType.edited? this.state.markUpEntitiesEditData.entities:item.entities}/>
              {
                this.state.status[index] === FilterElementType.edited &&
                <button className={cn("settings-training-table__accept-button", "settings-training__button")}
                        onClick={this.acceptTableRowEditing(index)}
                        disabled={!(this.state.markUpEntitiesEditData.area_of_testing && this.state.markUpEntitiesEditData.entities.length)}>
                  <Icon type={IconType.check} size={IconSize.normal}/>
                </button>
              }
            </div>

            {
              this.state.status[index] === FilterElementType.hovered &&
              <div className="settings-training-table-main-section__edit-wrapper">

                <button className={cn("settings-training-table-main__edit-button", "settings-training__button")}
                        onClick={this.editTableRowData(index)}
                        disabled={this.state.status.includes(FilterElementType.edited)}>
                  <Icon type={IconType.edit2} size={IconSize.normal}/>
                </button>

                <button className={cn("settings-training-table-main__delete-button", "settings-training__button")}
                        onClick={this.deleteTableRow(index)}>
                  <Icon type={IconType.delete} size={IconSize.normal}/>
                </button>

              </div>
            }

          </div>
          ))}
        </div>

        

        <div className="settings-training-bug-resolution">
          <p className="settings-training-bug-resolution__title">Bug Resolution</p>
          {Array(2).fill("").map((_,index)=>(
            <div key={index} className="settings-training-bug-resolution-wrapper">
              <div className={cn("settings-training-bug-resolution-metric","settings-training-table-input")}>
                <p className="settings-training-bug-resolution-metric__title">Metric</p>
                <InputElement type={FilterElementType.disabled}
                              placeholder={this.state.bug_resolution.resolution_settings[index].metric}/>
              </div>
              <div className={cn("settings-training-bug-resolution-value","settings-training-table-select")}>
                <p className="settings-training-bug-resolution-value__title">Value</p>
                <DropdownElement placeholder="Value"
                                 type={this.state.isAllowedEntitiesEditing? FilterElementType.simple: FilterElementType.disabled}
                                 dropDownValues={this.state.bug_resolution.resolution_names}
                                 excludeValues={bugResolutionExcludeValues.filter(item=>item!==this.state.bug_resolution.resolution_settings[index].value)}
                                 value={this.state.bug_resolution.resolution_settings[index].value}
                                 onChange={this.changeBugResolutionValue(index)}
                                 onClear={this.clearBugResolutionValue(index)}/>
              </div>
            </div>
          ))}

        </div>

        <div className="settings-training-footer">
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
                  disabled={ this.state.isSettingsDefault ||
                            !(this.state.isAllowedEntitiesEditing &&
                            this.state.markup_entities.mark_up_entities.length &&
                            this.state.bug_resolution.resolution_settings[0].value.trim().length &&
                            this.state.bug_resolution.resolution_settings[1].value.trim().length)}/>
        </div>

      </div>
    )
  }
}

const mapStateToProps = ({settings}: RootStore) => ({
  training: settings.settingsTrainingStore,
})

const mapDispatchToProps = {
  sendSettingsData, 
  sendSettingsTrainingData,
  uploadSettingsTrainingSubfieldData
}

const connector = connect(mapStateToProps, mapDispatchToProps)

type PropsFromRedux = ConnectedProps<typeof connector>;
type Props = PropsFromRedux & {};

export default connector(SettingsTraining)
