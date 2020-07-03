import React from "react";
import Icon, { IconSize, IconType } from 'app/common/components/icon/icon';
import "app/modules/virtual-assistant/message-input/message-input.scss"

interface MessageInputProps{
  message: string,
  inputMessage: (message: string)=>void,
  sendMessage: ()=>void,
}

export default function MessageInput(props: MessageInputProps)
{
  return(
    <div className="message-input">
      <input className="message-input__input"
             placeholder="Type a message here"
             value={props.message}
             onChange={(e)=>props.inputMessage(e.target.value)}
             onKeyPress={(e)=>{if(e.key==="Enter" && props.message.length) props.sendMessage()}}/>
      <button className="message-input__send-button"
              onClick={props.sendMessage}
              disabled={!props.message.length}>
        <Icon size={IconSize.normal} type={IconType.send}/>
      </button>
    </div>
  )
}
