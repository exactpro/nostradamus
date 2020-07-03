import React, { Component } from "react";
import cn from "classnames";
import {MessageDataUnion, MessageSendingType, InboundData, OutboundData, InboundButton, InboundReport} from "app/common/store/virtual-assistant/types";
import Icon, { IconSize, IconType } from 'app/common/components/icon/icon';
import "app/modules/virtual-assistant/message-viewer/message-viewer.scss";
// import chatPicture from "assets/images/chatPicture.png";

interface Props{
  messages: MessageDataUnion[],
  selectItem: (item: string) => () => void,
}

export default class MessageViewer extends Component<Props>{

  state={
    isChoiceListVisible: true,
  }

  renderMessage = (item: MessageDataUnion, index: number) => {
    let str: string | undefined = (item.content as OutboundData).message || (item.content as InboundData).text;
    if(!str) return;
    let linkArr: any;
    let linkRx: RegExp = /\[.*?\]\(.*?\)/g;

    linkArr=str.match(linkRx);

    if(linkArr)
    {
      let paragraphArr: string[] = str.split(linkRx).filter(Boolean);
      let linkTextRx: RegExp = /[^[]+(?=\])/g, linkRefRx: RegExp = /[^(]+(?=\))/g;
      return(
        <div key={index}
           className={cn("message-viewer-message",`message-viewer-message_${item.messageType}`)}>
           {
             paragraphArr.map((item:string, index: number)=>{
               let linkText: string | null = null, linkRef: string | null = null, link: any = linkArr[index];
               if(link) {
                 linkText = link.match(linkTextRx)[0];
                 linkRef = link.match(linkRefRx)[0];
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
      <p key={index}
         className={cn("message-viewer-message",`message-viewer-message_${item.messageType}`)}>
         {str}
      </p>)
  }

  renderChoiceList = (buttons: InboundButton[]) => (
    <div className={cn("message-viewer-choice-list",{"message-viewer-choice-list_hidden": !this.state.isChoiceListVisible})}>
      {
        buttons.map((item,index)=>(
          <button key={index} className="message-viewer-choice-list__item"
                  onClick={()=>{this.setState({isChoiceListVisible:false}); this.props.selectItem(item.title)();}}>
            {item.title}
          </button>
        ))}
    </div>)

  renderUploadFile = ({filename, format, link, size}: InboundReport, index: number) => (
    <div key={`UploadFile ${index}`} className={cn("message-viewer-file-upload",`message-viewer-file-upload_${MessageSendingType.inbound}`)}>
      <a className={"message-viewer-file-upload__title"}
         href={link} download>
        <button className={"message-viewer-file-upload__button"}>
          <Icon size={IconSize.normal} type={IconType.send}/>
        </button>
      </a>
      <div className={"message-viewer-file-upload__wrapper"}>
        <a className={"message-viewer-file-upload__title"}
           href={link} download>
            {filename}
        </a>
        <div className="message-viewer-file-upload__info">
          <p className={"message-viewer-file-upload__info-title"}>{size}</p>
          <p className={"message-viewer-file-upload__info-title"}>{format}</p>
        </div>
      </div>
    </div>
  )

  shouldComponentUpdate = (nextProps: Props) => {
    if(!this.state.isChoiceListVisible && this.props.messages.length !== nextProps.messages.length) this.setState({isChoiceListVisible:true})
    return true;
  }

  render(){
    let messages = this.props.messages.slice().reverse();
    let buttons = messages[0]? (messages[0].content as InboundData).buttons: undefined;

    return(
      <React.Fragment>
        <div className="message-viewer">
          {
            messages.length?
            messages.map((item: MessageDataUnion , index: number)=>{
              let report: InboundReport|undefined = (item.content as InboundData).custom;
              if(report) return this.renderUploadFile(report, index);
              return this.renderMessage(item, index);
            })
            :<div className="message-viewer__layout-image" />
            // style={{backgroundImage: `url(${chatPicture})`}}
          }
        </div>

        <div className="message-viewer-choice-wrapper">
          {
            buttons &&
            this.renderChoiceList(buttons)
          }
        </div>
      </React.Fragment>
    )
  }
}
