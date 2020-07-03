import React, {Component} from "react";
import cn from "classnames"
import InputElement from "app/modules/settings/elements/input-element/input-element";
import {FilterElementType} from "app/modules/settings/elements/elements-types";
import Icon, {IconSize, IconType} from "app/common/components/icon/icon";
import "app/modules/settings/elements/input-training-element/input-training-element.scss";

interface InputTrainingElementProps{
  type: FilterElementType,
  onChange: (value: string)=>void,
  onClear: (index: number) => void,
  values: string[],
  id: number,
}

export default class InputTrainingElement extends Component<InputTrainingElementProps>{

  state = {
    isOpen: false,
    isWrapperOpen: false,
    value: "",
  }

  spreadButtonRef: React.RefObject<HTMLButtonElement> = React.createRef();
  valueBlocksWrapperRef: React.RefObject<HTMLDivElement> = React.createRef();

  static defaultProps={
    type: FilterElementType.simple,
    values:[],
    onChange: ()=>{},
    onClear: ()=>{},
    id: 0,
  }

  onChangeHandler = (value: string) => {
    this.setState({value})
  }

  onClearHandler = () => {
    this.setState({value:""})
  }

  onFocusHandler = (e: any) => {
    e.currentTarget === e.target &&
    this.setState({
      isOpen: true,
    })
  }

  addValue=()=>{
    this.state.value && this.props.onChange(this.state.value)
    this.setState({
      isOpen:false,
      isWrapperOpen: false,
      value: ""
    })
  }

  onKeyPressHandler = (e: any) => {
    if(e.key==="Enter") this.addValue()
  }

  onBlurHandler = (e: any) => {
    if(![...e.currentTarget.children].includes(e.relatedTarget)) this.addValue()
  }

  renderValueBlock = (content: string, index: number, allowedEditing: boolean) => {
    return (
      <div key={index} className="input-training-element-value-block">
        <p className="input-training-element-value-block__number">{index+1}</p>
        <p className="input-training-element-value-block__content">{content}</p>
        {
          allowedEditing &&
          <button className="input-training-element-value-block__close"
                onClick={this.clearValueBlock(index)}>
          <Icon size={ IconSize.small } type={ IconType.close }/>
          </button>
        }
      </div>
    )
  }

  clearValueBlock = (index: number) => () => {
    this.props.onClear(index)
  }

  activateOverflawWrapper = () => {
    this.setState({isWrapperOpen:!this.state.isWrapperOpen})
  }

  valueBlockWrapperStatus = () => {
    if(this.valueBlocksWrapperRef.current && this.spreadButtonRef.current)
    {
      let hiddenBlocksNumber: number = 0;
      [].forEach.call(this.valueBlocksWrapperRef.current.children, (item: HTMLElement,_, array: HTMLElement[])=>{
        if(item && item.offsetTop > array[0].offsetTop){
          hiddenBlocksNumber++;
        }
      })

      if(this.state.isWrapperOpen){
        if(hiddenBlocksNumber){
          this.spreadButtonRef.current.innerHTML=`hide`;
        }
        else{
           this.spreadButtonRef.current.style.display="none";
           this.activateOverflawWrapper()
        }
      }
      else{

        if(hiddenBlocksNumber){
          this.spreadButtonRef.current.style.display="block";
          this.spreadButtonRef.current.innerHTML=`+${hiddenBlocksNumber} more`
        }
        else this.spreadButtonRef.current.style.display="none";
      }

    }
  }

  componentDidUpdate = (prevprops: InputTrainingElementProps) => {
    if(prevprops.type !== this.props.type && this.state.isWrapperOpen) this.setState({isWrapperOpen:false})
    this.valueBlockWrapperStatus()
  }


  render(){
    let allowedEditing = [FilterElementType.simple, FilterElementType.edited].includes(this.props.type)

    return(
      <div className="input-training-element">
        <button ref={this.spreadButtonRef}
                className="input-training-element__spread-button"
                onClick={this.activateOverflawWrapper}/>

        {
          this.state.isOpen?
            <div className="input-training-element__input-wrapper">
              <InputElement value={this.state.value}
                            type={this.props.type}
                            placeholder="Entities Name"
                            onChange={this.onChangeHandler}
                            onClear={this.onClearHandler}
                            onBlur={this.onBlurHandler}
                            onKeyPress={this.onKeyPressHandler}/>
            </div>:
            <div className={cn("input-training-element-block-container",`input-training-element-block-container_${this.props.type}`)}
                 ref={this.valueBlocksWrapperRef}
                 style={{height:this.state.isWrapperOpen? "auto": ""}}
                 onClick={allowedEditing? this.onFocusHandler: undefined}>
                    {!this.props.values.length && <p className="input-training-element-block-container__placeholder">Entities Name</p>}
                    {this.props.values.map((item,index)=>this.renderValueBlock(item, index, allowedEditing))}
            </div>
       }
       
      </div>
    )
  }
}
