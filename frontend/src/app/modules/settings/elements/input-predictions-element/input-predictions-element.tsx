import React, {Component} from "react";
import {PredictionTableType} from "app/common/store/settings/types";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import cn from "classnames";
import {FilterElementType} from "app/modules/settings/elements/elements-types";
import "app/modules/settings/elements/input-predictions-element/input-predictions-element.scss";

interface InputPredictionsElementProps{
  values: PredictionTableType[],
  onClear: (index: number) => () => void,
  onChange: (index: number, name: string) => void,
  onChangeOrder: (indexDrag: number, indexPaste: number) => void
}

export default class InputPredictionsElement extends Component<InputPredictionsElementProps>{

  state={
    type:FilterElementType.simple,
    editIndex: null,
    name: ""
  }

  dragRef: any = undefined

  startContentEdition = (index: number) => () => {
    if(this.props.values[index].is_default) return
    this.setState({
      type: FilterElementType.edited,
      editIndex: index,
      name: this.props.values[index].name})
  }

  stopContentEdition = () => {
    if(!this.state.name) return
    this.props.onChange(this.state.editIndex as unknown as number, this.state.name)
    this.setState({
      type: FilterElementType.simple,
      editIndex: null,
      name: ""
    })
  }

  editContent = ({target}: any) => {
    this.setState({name: target.value})
  }

  dragStart = (e: any) => {
    this.dragRef=e.target
    e.target.style.opacity="0.25"
  }

  dragEnd = (e: any) => {
    e.target.style.opacity="1"
  }

  dragOver = (e: any) => {
    e.preventDefault()
  }

  dragEnter = (e: any) => {
    //if(e.target.classList.contains(this.dragRef.classList[0]) && e.target!==this.dragRef) e.target.style.marginLeft="50px";
  }

  dragLeave = (e: any) => {
    //if(e.target.classList.contains(this.dragRef.classList[0]) && e.target!==this.dragRef) e.target.style.marginLeft="0";
  }

  onDrop = (e: any) => {
    let {target} = e
    while(target.classList[0] !== this.dragRef.classList[0]) target=target.parentNode
    this.props.onChangeOrder(
        Array.from(target.parentNode.children).indexOf(this.dragRef),
        Array.from(target.parentNode.children).indexOf(target))
  }

  render(){
    return(
      <div  className="input-predictions-element"
            onDragOver={this.dragOver}>
        {
          this.props.values.map((item,index)=>(
            <div  key={index}
                  onDragStart={this.dragStart}
                  onDragEnter={this.dragEnter}
                  onDragLeave={this.dragLeave}
                  onDragEnd={this.dragEnd}
                  onDrop={this.onDrop}
                  draggable={true}
                  tabIndex={1}
                  className={cn("input-predictions-element-block",
                                {"input-predictions-element-block_lock": item.is_default},
                                {"input-predictions-element-block_edited": index===this.state.editIndex && this.state.type === FilterElementType.edited})}>
              <p className="input-predictions-element-block__position">{item.position}</p>

              {
                index!==this.state.editIndex &&
                <p  className="input-predictions-element-block__content"
                    onClick={this.startContentEdition(index)}>
                      {item.name}
                </p>
              }

              {
                index===this.state.editIndex &&
                <input  className={cn("input-predictions-element-block__input","input-predictions-element-block__content")}
                        value={this.state.name}
                        style={{width:this.state.name.length+"ch"}}
                        onBlur={this.stopContentEdition}
                        onChange={this.editContent}/>
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
