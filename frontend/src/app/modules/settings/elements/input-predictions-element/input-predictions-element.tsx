import React, {Component} from "react";
import {PredictionTableData} from "app/common/store/settings/types";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import cn from "classnames";
import {FilterElementType} from "app/modules/settings/elements/elements-types";
import "app/modules/settings/elements/input-predictions-element/input-predictions-element.scss";

interface InputPredictionsElementProps{
  values: PredictionTableData[],
  onClear: (index: number) => () => void,
  onChange: (index: number, name: string) => void,
  onChangeOrder: (indexDrag: number, indexPaste: number) => void
}

interface InputPredictionsElementState{
  valueBlockType: FilterElementType,
  valueBlockIndex: number|null,
  valueBlockContent: string,
}

export default class InputPredictionsElement extends Component<InputPredictionsElementProps,InputPredictionsElementState>{

  constructor(props: InputPredictionsElementProps){
    super(props);
    this.state = this.getDefaultStateObject();
  }

  valueBlockRef: any = undefined;

  startValueBlockContentEdition = (index: number) => () => {
    if(this.props.values[index].is_default) return
    this.setState({
      valueBlockType: FilterElementType.edited,
      valueBlockIndex: index,
      valueBlockContent: this.props.values[index].name})
  }

  stopValueBlockContentEdition = () => {
    if(!this.state.valueBlockContent) return
    this.props.onChange(this.state.valueBlockIndex as unknown as number, this.state.valueBlockContent)
    this.setState(this.getDefaultStateObject())
  }

  editValueBlockContent = ({target}: any) => {
    this.setState({valueBlockContent: target.value})
  }

  valueBlockDragStart = (e: any) => {
    this.valueBlockRef=e.target
    e.target.style.opacity="0.25"
  }

  valueBlockDragEnd = (e: any) => {
    e.target.style.opacity="1"
  }

  valueBlockDragOver = (e: any) => {
    e.preventDefault()
  }

  valueBlockDrop = (e: any) => {
    let {target} = e
    while(target.classList[0] !== this.valueBlockRef.classList[0]) target=target.parentNode
    this.props.onChangeOrder(
        Array.from(target.parentNode.children).indexOf(this.valueBlockRef),
        Array.from(target.parentNode.children).indexOf(target))
  }

  getDefaultStateObject = () => ({
    valueBlockType: FilterElementType.simple,
    valueBlockIndex: null,
    valueBlockContent: ""
  })

  render(){
    return(
      <div  className="input-predictions-element"
            onDragOver={this.valueBlockDragOver}>
        {
          this.props.values.map((item,index)=>(
            <div  key={index}
                  onDragStart={this.valueBlockDragStart}
                  onDragEnd={this.valueBlockDragEnd}
                  onDrop={this.valueBlockDrop}
                  draggable={true}
                  tabIndex={1}
                  className={cn("input-predictions-element-block",
                                {"input-predictions-element-block_lock": item.is_default},
                                {"input-predictions-element-block_edited": index===this.state.valueBlockIndex && this.state.valueBlockType === FilterElementType.edited})}>
              <p className="input-predictions-element-block__position">{item.position}</p>

              {
                index!==this.state.valueBlockIndex &&
                <p  className="input-predictions-element-block__content"
                    onClick={this.startValueBlockContentEdition(index)}>
                      {item.name}
                </p>
              }

              {
                index===this.state.valueBlockIndex &&
                <input  className={cn("input-predictions-element-block__input","input-predictions-element-block__content")}
                        value={this.state.valueBlockContent}
                        style={{width:this.state.valueBlockContent.length+"ch"}}
                        onBlur={this.stopValueBlockContentEdition}
                        onChange={this.editValueBlockContent}/>
              }
              <button className="input-predictions-element-block__button"
                      onClick={item.is_default? undefined: this.props.onClear(index)}>
                    <Icon size={ IconSize.small } type={ item.is_default? IconType.lock: IconType.close }/>
              </button>
            </div>
          ))
        }
      </div>
    )
  }
}
