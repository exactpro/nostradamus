import React, {Component} from "react"
import  {FilterElementType} from "app/modules/settings/elements/elements-types"
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import cn from "classnames"
import "app/modules/settings/elements/dropdown-element/dropdown-element.scss";
import { caseInsensitiveStringCompare } from "app/common/functions/helper";

interface DropdownProps{
  type: FilterElementType,
  value: string,
  dropDownValues: string[],
  writable: boolean,
  excludeValues: string[],
  onChange: any,
  onClear: ()=>void,
  style?: React.CSSProperties,
  placeholder?: string,
}

interface DropdownState{
  inputValue: string,
  isDropDownWrapperOpened: boolean,
}

class DropdownElement extends Component<DropdownProps, DropdownState>{

  constructor(props: DropdownProps){
    super(props);
    this.state={
      inputValue: props.value,
      isDropDownWrapperOpened: false
    }
  }

  static defaultProps = {
    type: FilterElementType.simple,
    value: "", 
    writable: true,
    excludeValues: [],
    placeholder: "Type"
  }
 
  dropdownElementRef: React.RefObject<HTMLDivElement> = React.createRef();

  focusDropDownElement = (e: React.FocusEvent<HTMLDivElement>) => {  
    this.setState({isDropDownWrapperOpened: true});
  }

  blurDropDownElement = () => {  
    this.setState({isDropDownWrapperOpened: false});
  }

  selectDropdownOption = (inputValue: string) => () => { 
    this.setState({inputValue}, this.blurDropDownElement);
    this.props.onChange(inputValue);

    if(!this.props.writable && this.dropdownElementRef.current) this.dropdownElementRef.current.blur();
  }

  changeInputValue = (e: React.ChangeEvent<HTMLInputElement>) => {
    this.setState({inputValue: e.target.value});
  }

  clearInputValue = () => {
    this.setState({inputValue:""}, this.props.onClear)
  }

  shouldComponentUpdate = (nextProps: DropdownProps) => {
    if(!nextProps.value.length && this.props.value) this.setState({inputValue:""});
    if(nextProps.value !== this.props.value) this.setState({inputValue: nextProps.value});
    return true;
  }

  isStrIncludesSubstr = (str: string, substr: string) =>  str.toLowerCase().includes(substr.toLowerCase());

  render(){
    const allowedOpening: boolean = [FilterElementType.simple, FilterElementType.edited].includes(this.props.type);
    const isInputEditable: boolean = allowedOpening && this.props.writable;

    let dropDownOptions: string[] = [...this.props.dropDownValues];

    if(isInputEditable){
      dropDownOptions = dropDownOptions.filter((str: string)=>{ 
        if(this.state.inputValue.length) return this.isStrIncludesSubstr(str, this.state.inputValue) && !this.props.excludeValues?.includes(str);
        return true;
      })
    }
    
    dropDownOptions.sort((a, b) => caseInsensitiveStringCompare(a,b));
                  
    return (
      <div className="dropdown-element" tabIndex={1}
           ref={this.dropdownElementRef}
           onFocus={this.focusDropDownElement}
           onBlur={this.blurDropDownElement} 
           style={this.props.style}>

          <input value = {this.state.inputValue}
                 onChange={this.changeInputValue}
                 placeholder={this.props.placeholder}
                 disabled={!isInputEditable}
                 className={cn("dropdown-element__select",
                               "dropdown-element__select_"+this.props.type, 
                               {"dropdown-element__select_disabled": !this.props.value})}/>

          {
            allowedOpening &&
            <React.Fragment>
              {
                !!dropDownOptions.length && 
                <div  className={cn("dropdown-element-wrapper", {"dropdown-element-wrapper_hidden": !this.state.isDropDownWrapperOpened})}>
                  
                    {   
                      dropDownOptions.map((item,index)=>(
                        <div  className={cn("dropdown-element-wrapper__option", 
                                            {"dropdown-element-wrapper__option_disabled": !this.state.inputValue.length && this.props.excludeValues?.includes(item)})}
                              onClick={this.selectDropdownOption(item)} 
                              key={index}>
                          {item}
                        </div>
                      ))
                    }

                </div>
              }

              <Icon className={cn("dropdown-element__open", {"dropdown-element__open_rotated": this.state.isDropDownWrapperOpened} )} 
                    size={IconSize.small} type={IconType.down}/>
              <button className="dropdown-element__clear-value"
                      onClick={this.clearInputValue}>
                <Icon  size={IconSize.small} type={IconType.close}/>
              </button>
            </React.Fragment>
          }

      </div>
    )
  }
}

export default DropdownElement
