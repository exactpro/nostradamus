import React, {Component} from "react";
import cn from "classnames" 
import {FilterElementType, FilterDropdownType} from "app/modules/settings/elements/elements-types";
import SelectWindow from "app/modules/settings/elements/select-window/select-window";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import "app/modules/settings/elements/input-training-element/input-training-element.scss";

interface InputTrainingElementProps{
  type: FilterElementType,
  onChange: (value: string)=>void,
  onClear: (index: number) => void,
  onClearAll: () => void,
  values: string[],
  dropDownValues: string[],
}

interface InputTrainingElementState{
  isSelectWindowOpen: boolean,
  isSelectedListOpen: boolean,
  quickSearchValue: string
}

export default class InputTrainingElement extends Component<InputTrainingElementProps, InputTrainingElementState>{

  constructor(props: InputTrainingElementProps){
    super(props);

    this.state = {
      isSelectWindowOpen:false,
      isSelectedListOpen: false,
      quickSearchValue: "",
    };
  }

  static defaultProps={
    type: FilterElementType.simple,
    dropDownValues: Object.values(FilterDropdownType),
  }

  timerID: NodeJS.Timeout | null = null;
  inputTrainingElementRef: React.RefObject<HTMLDivElement> = React.createRef();
  allowedEditing: boolean = false;

  changeQuickSearchValue = (e: React.ChangeEvent<HTMLInputElement>) => {
    this.setState({quickSearchValue: e.target.value});
  }

  onFocusTrainingElement = () => {
    if(!this.allowedEditing) return;
    if(this.timerID) clearTimeout(this.timerID);
    this.setState({isSelectWindowOpen: true})
  };

  onBlurTrainingElement = () => {
    this.timerID = setTimeout(()=>this.setState({isSelectWindowOpen: false,
                                                 isSelectedListOpen: false}), 0)
  };

  openSelectedValuesList = () => {
    this.setState({
      isSelectedListOpen: !this.state.isSelectedListOpen, 
    })
  };

  selectDropdownValue = (value: string, isChecked: boolean) => () => {
    if(isChecked) { 
      this.deleteValueBlock(this.props.values.findIndex(item=>item===value))();
      return;
    }
    this.props.onChange(value);
  }

  deleteValueBlock = (index: number) => () => {
    if(this.props.values.length===1 && this.state.isSelectedListOpen) this.inputTrainingElementRef.current?.blur();
    this.props.onClear(index);
  }

  deleteAllValueBlocks = () => {
    this.props.onClearAll();
  }

  renderValueBlocks = (content: string, index: number) => {
    return (
      <div key={index} className="input-training-element-value-block">
        <div className="input-training-element-value-block__wrapper">
          <p className="input-training-element-value-block__number">{index+1}</p>
          <p className="input-training-element-value-block__content">{content}</p>
          {
            this.allowedEditing &&
            <button className="input-training-element-value-block__close"
                  onClick={this.deleteValueBlock(index)}>
            <Icon size={ IconSize.small } type={ IconType.close }/>
            </button>
          }
        </div>
      </div>
    )
  }

  isStrIncludesSubstr = (str: string, substr: string) =>  str.toLowerCase().includes(substr.toLowerCase());

  render(){
    
    this.allowedEditing = [FilterElementType.simple, FilterElementType.edited].includes(this.props.type)
    
    let values = this.props.values;
    let dropdownValues = this.state.isSelectedListOpen? this.props.values: this.props.dropDownValues;
    
    return(
      <div className="input-training-element"
           tabIndex={0}
           onFocus={this.onFocusTrainingElement}
           onBlur={this.onBlurTrainingElement}
           ref={this.inputTrainingElementRef}>
        
        {
          this.allowedEditing && 
          <div className="input-training-element-icons">
            <button className="input-training-element-icons__close"
                    onClick={this.deleteAllValueBlocks}>
              <Icon size={IconSize.small} type={IconType.close}/>
            </button>
            <Icon className={cn("input-training-element-icons__down",
                                {"input-training-element-icons__down_rotated": this.state.isSelectWindowOpen})} 
                  size={IconSize.small}
                  type={IconType.down}/>        
          </div>
        }        

        <div className={cn("input-training-element-block-container", "input-training-element-block-container_"+this.props.type)}>
          {
            values.length?
              [...values].splice(0,2).map((item,index)=>this.renderValueBlocks(item, index))
              :<p className="input-training-element-block-container__placeholder">Entities Name</p>
          }
        </div>

        {
          values.length>2 && this.allowedEditing && 
          <button className="input-training-element__spread-button"
                  onClick={this.openSelectedValuesList}> 
            + {values.length-2} more 
          </button>
        }

        {
          this.state.isSelectWindowOpen &&
          <div className="input-training-element__select-window">
            <SelectWindow selectWindowAllValues={dropdownValues}
                          selectWindowCheckedValues={values}
                          searchable={!this.state.isSelectedListOpen}
                          onSelectValue={this.selectDropdownValue}/>
          </div>
        }
        
      </div>
    )
  }
}
