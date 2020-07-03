import React, {Component} from "react";
import "app/modules/settings/fields/settings_training/settings_training.scss";
import InputElement from "app/modules/settings/elements/input-element/input-element";
import InputTrainingElement from "app/modules/settings/elements/input-training-element/input-training-element";
import {FilterElementType} from "app/modules/settings/elements/elements-types";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import Button, { ButtonStyled } from 'app/common/components/button/button';
import {MarkUpEntities, BugResolution, SettingsSections} from "app/common/store/settings/types";
import {connect, ConnectedProps} from "react-redux";
import {RootStore} from "app/common/types/store.types";
import {sendSettings} from "app/common/store/settings/thunks";
import cn from "classnames";

interface SettingsTrainingState{
  [key: string]: boolean|string|MarkUpEntities|Array<FilterElementType|MarkUpEntities|BugResolution>,
  mark_up_source: string,
  mark_up_entities: MarkUpEntities[],
  bug_resolution: BugResolution[],
  markUpEntitiesInputData: MarkUpEntities,
  markUpEntitiesEditData: MarkUpEntities,
  status: FilterElementType[],
  isSettingsDefault: boolean,
}

class SettingsTraining extends Component<Props>{

  state:SettingsTrainingState={
    mark_up_source: "",
    mark_up_entities: [],
    bug_resolution:[],
    markUpEntitiesInputData:{
      area_of_testing:"",
      entities:[]
    },
    markUpEntitiesEditData:{
      area_of_testing:"",
      entities:[]
    },
    status:[],
    isSettingsDefault: true,
  }

  constructor(props: Props)
  {
    super(props)
    this.state.mark_up_source = props.training.mark_up_source;
    this.state.mark_up_entities = [...props.training.mark_up_entities];
    this.state.bug_resolution = this.setBugResolution();
    this.state.status = props.training.mark_up_entities.map((_:any,index:number)=>this.getTableElementStatus(index));
  }

  setBugResolution = ():BugResolution[] => {
    switch (this.props.training.bug_resolution.length) {
      case 0:
        return [{metric: "Resolution", value:""}, {metric: "Resolution", value:""}] ;
      case 1:
        return [{...this.props.training.bug_resolution[0]}, {metric: "Resolution", value:""}];
      default:
        return [{...this.props.training.bug_resolution[0]},{...this.props.training.bug_resolution[1]}];
    }
  }

  setMarkUpEntitiesData = (keyField: string,valField: string) => (value: string) => {
    let data: MarkUpEntities = this.state[keyField] as MarkUpEntities;
    if(valField==="area_of_testing") data.area_of_testing = value;
    else data.entities.push(value);
    this.setState({[keyField]: data});
  }

  clearMarkUpEntitiesInputData = (keyField: string) => () => {
    let data: MarkUpEntities = this.state[keyField] as MarkUpEntities;
    data["area_of_testing"] = "";
    this.setState({[keyField]:data});
  }

  clearMarkUpEntitiesBlockValueData = (keyField: string) => (index: number) => {
    let data: MarkUpEntities = this.state[keyField] as MarkUpEntities;
    data.entities.splice(index,1);
    this.setState({[keyField]:data});
  }

  addPosition = () => {
    let {mark_up_entities, markUpEntitiesInputData, status} = this.state;
    mark_up_entities.push({...markUpEntitiesInputData});
    markUpEntitiesInputData={
      area_of_testing:"",
      entities:[],
    };
    status.push(mark_up_entities.length%2===0? FilterElementType.odd: FilterElementType.even);
    this.setState({
      mark_up_entities,
      markUpEntitiesInputData,
      status,
    });
    this.detectIsSettingsDefault();
  }

  setMarkUpSource = (mark_up_source: string) => {
    this.setState({mark_up_source});
    this.detectIsSettingsDefault();
  }

  clearMarkUpSource = () => {
    this.setState({mark_up_source:""});
    this.detectIsSettingsDefault();
  }

  changeBugResolutionValue = (index: number) => (value: string) => {
    let bug_resolution: BugResolution[] | BugResolution= this.state.bug_resolution as BugResolution[];
    bug_resolution[index]={
      metric: bug_resolution[index]? bug_resolution[index].metric: "Resolution",
      value:value
    };
    this.setState({
        bug_resolution,
      });
    this.detectIsSettingsDefault();
  }

  clearBugResolutionValue = (index: number) => () => {
    let {bug_resolution} = this.state;
    if(bug_resolution[index]){
      bug_resolution[index].value="";
      this.setState({bug_resolution});
      this.detectIsSettingsDefault();
    }
  }

  changeHoverStatus = (index: number) => ({type}: any) => {
    let {status} = this.state
    if(status[index]!==FilterElementType.edited)
    switch (type) {
      case "mouseenter":
        status[index] = FilterElementType.hovered;
        break;
      default:
        status[index] = this.getTableElementStatus(index);
        break;
    }
    this.setState({status})
  }

  getTableElementStatus = (index: number) => index%2===1? FilterElementType.odd: FilterElementType.even

  editPosition = (index: number) => async () => {
    let {status, markUpEntitiesEditData} = this.state;

    status.forEach((item: FilterElementType, itemIndex: number) => {
      if(item===FilterElementType.edited) status[itemIndex] = this.getTableElementStatus(itemIndex);
    });

    status[index]=FilterElementType.edited;
    markUpEntitiesEditData.area_of_testing = this.state.mark_up_entities[index].area_of_testing;
    markUpEntitiesEditData.entities = [...this.state.mark_up_entities[index].entities];
    this.setState({status, markUpEntitiesEditData});
  }

  acceptEditing = (index: number) => () => {
    let {status, markUpEntitiesEditData, mark_up_entities} = this.state;
    status[index] = this.getTableElementStatus(index);
    mark_up_entities[index]= markUpEntitiesEditData;
    markUpEntitiesEditData={
      area_of_testing:"",
      entities:[],
    };
    this.setState({
      status,
      mark_up_entities,
      markUpEntitiesEditData,
    });
    this.detectIsSettingsDefault();
  }

  deletePosition = (index: number) => () => {
    let {mark_up_entities, status} = this.state;
    mark_up_entities.splice(index,1);
    status.pop();
    this.setState({
      mark_up_entities,
      status,
    });
    this.detectIsSettingsDefault();
  }

  saveSettings = () => {
    this.detectIsSettingsDefault(true);
    let settings = {
      mark_up_source:this.state.mark_up_source,
      mark_up_entities:[...this.state.mark_up_entities],
      bug_resolution:[...this.state.bug_resolution]
    };

    this.props.sendSettings(
      SettingsSections.training,
      settings);
  }

  clearSettings = () => {
    this.setState({
      mark_up_source: this.props.training.mark_up_source,
      mark_up_entities: [...this.props.training.mark_up_entities],
      bug_resolution: this.setBugResolution(),
      markUpEntitiesInputData:{
        area_of_testing:"",
        entities:[]
      },
      markUpEntitiesEditData:{
        area_of_testing:"",
        entities:[]
      },
      status: this.props.training.mark_up_entities.map((_:any,index:number)=>this.getTableElementStatus(index)),
    });
    this.detectIsSettingsDefault(true);
  }

  detectIsSettingsDefault = (isSettingsDefault: boolean = false) => this.setState({isSettingsDefault})

  render(){
    return(
      <div className="settings-training">
        <p className="settings-training__title">Training</p>

        <div className="settings-training-source">
          <p className="settings-training-source__title">Mark Up Source</p>
          <InputElement type={FilterElementType.simple}
                        value={this.state.mark_up_source}
                        placeholder="Source"
                        onChange={this.setMarkUpSource}
                        onClear={this.clearMarkUpSource}
                        style={{width:"40%"}}/>
        </div>


        <div className="settings-training-table-header">

          <p className="settings-training-table-header__title">Mark Up Entities</p>

          <div className="settings-training-table-header__wrapper">
            <div className="settings-training-table-input">
              <p className="settings-training-table-header__field-title">Area of Testing</p>
              <InputElement type={FilterElementType.simple}
                            value={this.state.markUpEntitiesInputData.area_of_testing}
                            placeholder="Area"
                            onChange={this.setMarkUpEntitiesData("markUpEntitiesInputData" ,"area_of_testing")}
                            onClear={this.clearMarkUpEntitiesInputData("markUpEntitiesInputData")}
                            style={{width:"90%"}}/>
            </div>

            <div className="settings-training-table-select">
              <p className="settings-training-table-header__field-title">Entities</p>
              <div className="settings-training-table-select__select-wrapper">
                <InputTrainingElement onChange={this.setMarkUpEntitiesData("markUpEntitiesInputData", "entities")}
                                      onClear={this.clearMarkUpEntitiesBlockValueData("markUpEntitiesInputData")}
                                      values={this.state.markUpEntitiesInputData.entities}/>
                <button className={cn("settings-training__add-position", "settings-training__button")}
                        onClick={this.addPosition}
                        disabled={!(this.state.markUpEntitiesInputData.area_of_testing && this.state.markUpEntitiesInputData.entities.length)}>
                  <Icon size={IconSize.small} type={IconType.close}/>
                </button>
              </div>
            </div>
          </div>

        </div>



        <div className="settings-training-table-main">
          {this.state.mark_up_entities.map((item:any,index: number)=>(
          <div  key={index} className="settings-training-table-main-section"
                onMouseEnter={this.changeHoverStatus(index)}
                onMouseLeave={this.changeHoverStatus(index)}>
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
                                    values={this.state.status[index]===FilterElementType.edited? this.state.markUpEntitiesEditData.entities:item.entities}
                                    id={index+1}/>
              {
                this.state.status[index] === FilterElementType.edited &&
                <button className={cn("settings-training-table__accept-button", "settings-training__button")}
                        onClick={this.acceptEditing(index)}
                        disabled={!(this.state.markUpEntitiesEditData.area_of_testing && this.state.markUpEntitiesEditData.entities.length)}>
                  <Icon type={IconType.check} size={IconSize.normal}/>
                </button>
              }
            </div>

            {
              this.state.status[index] === FilterElementType.hovered &&
              <div className="settings-training-table-main-section__edit-wrapper">

                <button className={cn("settings-training-table-main__edit-button", "settings-training__button")}
                        onClick={this.editPosition(index)}
                        disabled={false}>
                  <Icon type={IconType.edit2} size={IconSize.normal}/>
                </button>

                <button className={cn("settings-training-table-main__delete-button", "settings-training__button")}
                        onClick={this.deletePosition(index)}>
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
                              placeholder={this.state.bug_resolution[index]? this.state.bug_resolution[index].metric: "Resolution"}/>
              </div>
              <div className={cn("settings-training-bug-resolution-value","settings-training-table-select")}>
                <p className="settings-training-bug-resolution-value__title">Value</p>
                <InputElement placeholder="Value"
                              value={this.state.bug_resolution[index]? this.state.bug_resolution[index].value: ""}
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
                  onClick={this.clearSettings}
                  disabled={this.state.isSettingsDefault}/>
          <Button text="Save Changes"
                  icon={IconType.check}
                  iconSize={IconSize.normal}
                  onClick={this.saveSettings}
                  disabled={this.state.isSettingsDefault ||
                            !(this.state.mark_up_source.trim().length &&
                            this.state.mark_up_entities.length &&
                            this.state.bug_resolution[0].value.trim().length &&
                            this.state.bug_resolution[1].value.trim().length)}/>
        </div>

      </div>
    )
  }
}

const mapStateToProps = ({settings}: RootStore) => ({
  training: settings.defaultSettings.training,
})

const mapDispatchToProps = {
  sendSettings,
}

const connector = connect(mapStateToProps, mapDispatchToProps)

type PropsFromRedux = ConnectedProps<typeof connector>;
type Props = PropsFromRedux & {};

export default connector(SettingsTraining)
