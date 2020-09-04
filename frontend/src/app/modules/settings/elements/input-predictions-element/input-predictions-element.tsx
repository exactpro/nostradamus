import React, {Component} from "react";
import {PredictionTableData} from "app/common/store/settings/types";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import cn from "classnames"; 
import "app/modules/settings/elements/input-predictions-element/input-predictions-element.scss";

interface InputPredictionsElementProps{
  values: PredictionTableData[],
  onDeletePrediction: (index: number) => () => void, 
  onChangeOrder: (indexDrag: number, indexPaste: number) => void
}

export default class InputPredictionsElement extends Component<InputPredictionsElementProps>{

  valueBlockRef: HTMLDivElement | undefined = undefined;

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
    if(!this.valueBlockRef) return
    
    let {target} = e
    while(target.classList[0] !== this.valueBlockRef.classList[0]) target=target.parentNode
    this.props.onChangeOrder(
        Array.from(target.parentNode.children).indexOf(this.valueBlockRef),
        Array.from(target.parentNode.children).indexOf(target))
  } 

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
                                {"input-predictions-element-block_lock": item.is_default})}>
             
              <p className="input-predictions-element-block__position">
                {item.position}
              </p>
             
              <p  className="input-predictions-element-block__content">
                    {item.name}
              </p>

              <button className="input-predictions-element-block__button"
                      onClick={item.is_default? undefined: this.props.onDeletePrediction(index)}>
                    <Icon size={ IconSize.small } type={ item.is_default? IconType.lock: IconType.close }/>
              </button>
            </div>
          ))
        }
      </div>
    )
  }
}
