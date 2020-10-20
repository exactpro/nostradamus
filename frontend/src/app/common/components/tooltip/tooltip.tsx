import React, { CSSProperties } from "react"
import { Timer } from 'app/common/functions/timer';
import PopupComponent, {ChildPosition} from "app/common/components/popup-component/popup-component";
import cn from "classnames"

import "./tooltip.scss"

enum TooltipWrapperShowing{
  hide = "hided",
  display = "visible",
}

export enum TooltipPosition{
  top = "top",
  bottom = "bottom",
  left = "left",
  right = "right",
}

interface TooltipProps{
  duration: number,
  message: string,
  position: TooltipPosition,
  children: React.ReactNode,
  isDisplayed: boolean, 
  style?: CSSProperties,
  tooltipOuterRef?: React.RefObject<HTMLDivElement>
}

interface TooltipState{
  wrapperDisplayStyle: TooltipWrapperShowing
}

// Change tooltip adding approach

class Tooltip extends React.Component<TooltipProps, TooltipState> {

  state: Readonly<TooltipState> =
    {
      wrapperDisplayStyle: TooltipWrapperShowing.hide,
    };

  static defaultProps = {
    duration: 2000, 
    position: TooltipPosition.top,
    isDisplayed: true, 
  }

  timer: any = {}; 

  hideTooltip = () => {

    this.setState({
      wrapperDisplayStyle: TooltipWrapperShowing.hide,
    })

  }

  displayTooltip = () => {
    
    if( this.timer.timerId ) this.timer.close()
    this.timer = new Timer(this.hideTooltip , this.props.duration as number)
    this.timer.pause()

    this.setState({
      wrapperDisplayStyle: TooltipWrapperShowing.display,
    })

  }

  render(){ 
      return(
        <div className="tooltip">
          <PopupComponent isChildDisplayed={this.state.wrapperDisplayStyle === TooltipWrapperShowing.display}
                          childPosition = {ChildPosition.top}
                          parent={
                            <div className={cn({"tooltip__wrapped-object":this.props.isDisplayed})}
                                onMouseEnter={this.displayTooltip}
                                onMouseLeave={this.timer.resume}>
                              {this.props.children}
                            </div>
                          }
                          child={
                            <div className={cn("tooltip-wrapper",
                                              {"tooltip-wrapper_displayed": this.props.isDisplayed},
                                              "tooltip-wrapper_"+this.props.position, 
                                              "tooltip-wrapper_"+this.state.wrapperDisplayStyle)} 
                                  style={this.props.style}
                                  onMouseEnter={this.timer.pause}
                                  onMouseLeave={this.timer.resume}
                                  ref={this.props.tooltipOuterRef}>

                              <div className="tooltip-wrapper__content">{this.props.message}</div>
                              <div className={cn("tooltip-wrapper__triangle", "tooltip-wrapper__triangle_"+this.props.position)}></div>

                            </div>
                          }/>
        </div>
      )
  }
}

export default Tooltip
