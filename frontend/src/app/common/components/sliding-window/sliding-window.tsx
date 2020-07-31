import React from "react";
import cn from "classnames";
import Icon, { IconSize, IconType } from 'app/common/components/icon/icon';
import "app/common/components/sliding-window/sliding-window.scss";

interface Props{
  title: string,
  isOpen: boolean,
  onClose: ()=>void,
  children?: React.ReactNode
}

export default function SlidingWindow(props: Props)
{
  return(
    <div className="sliding-window">

      {props.isOpen && <div className="sliding-window__underlayer" onClick={props.onClose}/>}

      <div className={cn("sliding-window-wrapper", {"sliding-window-wrapper_open": props.isOpen})}>

        <button className = "sliding-window-wrapper__close-button"
                onClick={props.onClose}>
          <Icon type={IconType.close} size={IconSize.small} />
        </button>

          <div className="sliding-window-wrapper__page">
            <p className="sliding-window-wrapper__title">{props.title}</p>
            <div className="sliding-window-wrapper__content">
              {props.children}
            </div>
          </div>

        </div>

    </div>
  )
}
