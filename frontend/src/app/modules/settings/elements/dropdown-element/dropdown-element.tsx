import React, {Component} from "react"
import  {FilterElementType, FilterDropdownType} from "app/modules/settings/elements/elements-types"
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import cn from "classnames"
import "app/modules/settings/elements/dropdown-element/dropdown-element.scss";

interface DropdownProps{
  type: FilterElementType,
  value: string,
  onChange?: any,
  onClear?: ()=>void,
}

class DropdownElement extends Component<DropdownProps>{

  static defaultProps = {
    type: FilterElementType.simple,
    value: ""
  }

  render(){
    let allowedOpening: boolean = [FilterElementType.simple, FilterElementType.edited].includes(this.props.type)
    return (
      <div className="dropdown-element" tabIndex={1}>

          <div className={cn("dropdown-element__select","dropdown-element__select_"+this.props.type, {"dropdown-element__select_disabled": !this.props.value})}>
            {this.props.value? this.props.value: "Type"}
          </div>

          {
            allowedOpening &&
            <>
              <div className={cn("dropdown-element-wrapper", "dropdown-element-wrapper_"+this.props.type)}>
                  {Object.values(FilterDropdownType).map((item,index)=>(
                      <div  className={cn("dropdown-element-wrapper__option" ,"dropdown-element-wrapper__option_"+this.props.type)}
                            onClick={()=>this.props.onChange(item)}
                            key={index}>
                        {item}
                      </div>
                  ))}
              </div>

              <Icon className="dropdown-element__open" size={IconSize.small} type={IconType.down}/>
              <button className="dropdown-element__clear-value"
                      onClick={this.props.onClear}>
                <Icon  size={IconSize.small} type={IconType.close}/>
              </button>
            </>
          }

      </div>
    )
  }
}

export default DropdownElement
