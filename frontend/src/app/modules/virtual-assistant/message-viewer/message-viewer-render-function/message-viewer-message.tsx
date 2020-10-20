import React from "react";
import { MessageDataUnion, OutboundData, InboundData } from "app/common/store/virtual-assistant/types";
import cn from "classnames";

interface MessageViewerMessageProps{
    messageItem: MessageDataUnion
}

export default function MessageViewerMessage(props: MessageViewerMessageProps){
    
    const message: string | undefined = (props.messageItem.content as OutboundData).message || (props.messageItem.content as InboundData).text;
    if(!message) return null;
    // the common pattern to render app's link is [link text](link ref), example: [follow the link](http://localhost/)
    const linkRegex: RegExp = /\[.*?\]\(.*?\)/g;

    const linkArr: any = message.match(linkRegex);

    // if link is found in message, then divide initial message by the link pattern and render in pairs [text that isn't the link that has been gotten by the division] - [the link]
    if(linkArr)
    {
      const textArr: string[] = message.split(linkRegex);
      
      const linkTextRegex: RegExp = /[^[]+(?=\])/g, linkRefRegex: RegExp = /[^(]+(?=\))/g;
      
      return(
        <div className={cn("message-viewer-message",`message-viewer-message_${props.messageItem.messageType}`)}>
           {
             textArr.map((item:string, index: number)=>{
               let linkText: string | null = null, linkRef: string | null = null, link: any = linkArr[index];
               if(link) {
                 linkText = link.match(linkTextRegex)[0];
                 linkRef = link.match(linkRefRegex)[0];
               }
               return(
                 <React.Fragment key={index}>
                  <p  className="message-viewer-message__link-text">{item}</p>
                  {(linkText && linkRef) && <a className="message-viewer-message__link-ref" href={linkRef} target="_blank" rel="noopener noreferrer">{linkText}</a>}
                 </React.Fragment>
               )
             })
           }
        </div>)
    }

    return(
      <p className={cn("message-viewer-message",`message-viewer-message_${props.messageItem.messageType}`)}>
         {message}
      </p>)
}