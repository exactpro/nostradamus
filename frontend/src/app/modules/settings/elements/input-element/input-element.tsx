import React, {Component} from "react"
import "app/modules/settings/elements/input-element/input-element.scss"
import  {FilterElementType} from "app/modules/settings/elements/elements-types"
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import cn from "classnames"

interface InputElementProps{
  type: FilterElementType,
  placeholder: string,
  style: Object,
  value: string,
  onChange: (value: string)=>void,
  onClear?: ()=>void,
  onKeyPress?: (e: any)=>void,
  onBlur?: (e: any) => void,
}

class InputElement extends Component<InputElementProps>{

  static defaultProps={
    type: FilterElementType.simple,
    placeholder: "Name",
    onChange: ()=>{},
    value: "",
    style: {},
  }

  render(){
    let allowedClearing: boolean = [FilterElementType.simple, FilterElementType.edited].includes(this.props.type)
    return (
      <div  className="input-element"
            style={ this.props.style }
            tabIndex={1}
            onBlur={this.props.onBlur}>
        <input  className={ cn("input-element__input", "input-element__input_"+this.props.type) }
                placeholder={ this.props.placeholder }
                value={this.props.value}
                disabled={ ![FilterElementType.simple, FilterElementType.edited].includes(this.props.type) }
                onChange={(event:any)=>this.props.onChange(event.target.value)}
                onKeyPress={this.props.onKeyPress}/>
        {
          allowedClearing &&
          <button className="input-element__close"
                  onClick={this.props.onClear}>
            <Icon size={ IconSize.small } type={ IconType.close }/>
          </button>
        }
      </div>
    )
  }
}

export default InputElement
