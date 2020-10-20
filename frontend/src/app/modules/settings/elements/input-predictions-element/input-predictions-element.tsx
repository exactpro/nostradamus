import React, {Component} from "react";
import {PredictionTableData} from "app/common/store/settings/types";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import cn from "classnames"; 
import "app/modules/settings/elements/input-predictions-element/input-predictions-element.scss";

interface InputPredictionsElementProps{
  values: PredictionTableData[],
  onDeletePrediction: (index: number) => () => void, 
  onChangePredictionsOrder: (indexDrag: number, indexPaste: number) => void
}

export default class InputPredictionsElement extends Component<InputPredictionsElementProps>{

  predictionBlockRef: HTMLDivElement | undefined = undefined;

  predictionBlockDragStart = ({target}: any) => {
    this.predictionBlockRef=target
    target.style.opacity="0.25"
  }

  predictionBlockDragEnd = ({target}: any) => {
    target.style.opacity="1"
  }

  predictionBlockDragOver = (e: any) => {
    e.preventDefault()
  }

  predictionBlockDrop = ({target}: any) => {
    if(!this.predictionBlockRef) return
    
    while(target.classList[0] !== this.predictionBlockRef.classList[0]) target=target.parentNode
    this.props.onChangePredictionsOrder(
        Array.from(target.parentNode.children).indexOf(this.predictionBlockRef),
        Array.from(target.parentNode.children).indexOf(target))
  } 

  render(){
    return(
      <div  className="input-predictions-element"
            onDragOver={this.predictionBlockDragOver}>
        {
          this.props.values.map((item,index)=>(
            <div  key={index}
                  onDragStart={this.predictionBlockDragStart}
                  onDragEnd={this.predictionBlockDragEnd}
                  onDrop={this.predictionBlockDrop}
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
