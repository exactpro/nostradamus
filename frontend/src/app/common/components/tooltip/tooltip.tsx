import React from "react"
import { Timer } from 'app/common/functions/timer';
import cn from "classnames"

import "./tooltip.scss"

enum TooltipWrapperShowing{
  hide = "hided",
  display = "displayed",
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
  children: React.ReactNode
}

interface TooltipState{
  wrapperDisplayStyle: TooltipWrapperShowing
}

class Tooltip extends React.Component<TooltipProps, TooltipState> {

  state: Readonly<TooltipState> =
    {
      wrapperDisplayStyle: TooltipWrapperShowing.hide,
    };

  static defaultProps = {
    duration: 2000, 
    position: TooltipPosition.top,
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

            <div className="tooltip__wrapped-object"
                 onMouseEnter={this.displayTooltip}
                 onMouseLeave={this.timer.resume}>
              {this.props.children}
            </div>

            <div className={cn("tooltip-wrapper", "tooltip-wrapper_"+this.props.position, "tooltip-wrapper_"+this.state.wrapperDisplayStyle)}
                 onMouseEnter={this.timer.pause}
                 onMouseLeave={this.timer.resume}>

                <div className="tooltip-wrapper__content">{this.props.message}</div>
                <div className={cn("tooltip-wrapper__triangle", "tooltip-wrapper__triangle_"+this.props.position)}></div>

            </div>

        </div>
      )
  }
}

export default Tooltip
