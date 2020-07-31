import React, { Component } from "react";
import cn from "classnames";
import {MessageDataUnion, MessageSendingType, InboundData, OutboundData, InboundChoiceList, InboundReport} from "app/common/store/virtual-assistant/types";
import Icon, { IconSize, IconType } from 'app/common/components/icon/icon';
import "app/modules/virtual-assistant/message-viewer/message-viewer.scss";
import chatPicture from "assets/images/chatPicture.png";

interface Props{
  messages: MessageDataUnion[],
  selectItem: (item: string) => () => void,
}

export default class MessageViewer extends Component<Props>{

  state={
    isChoiceListVisible: true,
  }

  renderMessage = (messageItem: MessageDataUnion, index: number) => {
    let message: string | undefined = (messageItem.content as OutboundData).message || (messageItem.content as InboundData).text;
    if(!message) return;
    let linkArr: any;
    // the common pattern to render app's link is [link text](link ref), example: [follow the link](http://localhost/)
    let linkRegex: RegExp = /\[.*?\]\(.*?\)/g;

    linkArr=message.match(linkRegex);

    // if link is found in message, then divide initial message by the link pattern and render in pairs [text that isn't the link that has been gotten by the division] - [the link]
    if(linkArr)
    {
      let textArr: string[] = message.split(linkRegex);
      let linkTextRegex: RegExp = /[^[]+(?=\])/g, linkRefRegex: RegExp = /[^(]+(?=\))/g;
      return(
        <div key={index}
           className={cn("message-viewer-message",`message-viewer-message_${messageItem.messageType}`)}>
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
      <p key={index}
         className={cn("message-viewer-message",`message-viewer-message_${messageItem.messageType}`)}>
         {message}
      </p>)
  }

  selectChoiceListItem = (message: string) => () => {
    this.setState({ isChoiceListVisible: false });
    setTimeout(this.props.selectItem(message), 200);
  }

  renderChoiceList = (choiceList: InboundChoiceList[]) => (
    <div className={cn("message-viewer-choice-list",{"message-viewer-choice-list_hidden": !this.state.isChoiceListVisible})}>
      {
        choiceList.map((item,index)=>(
          <button key={index} className="message-viewer-choice-list__item"
                  onClick={this.selectChoiceListItem(item.title)}>
            {item.title}
          </button>
        ))}
    </div>)

  renderUploadFile = ({filename, format, link, size}: InboundReport, index: number) => (
    <div key={`UploadFile ${index}`} className={cn("message-viewer-file-upload",`message-viewer-file-upload_${MessageSendingType.inbound}`)}>
      <a className={"message-viewer-file-upload__title"}
         href={link} download>
        <button className={"message-viewer-file-upload__button"}>
          <Icon size={IconSize.normal} type={IconType.file}/>
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
    if(!this.state.isChoiceListVisible && this.props.messages.length !== nextProps.messages.length) this.setState({isChoiceListVisible:true});
    return true;
  }

  render(){
    let messages = this.props.messages.slice().reverse();
    let choiceList = messages[0]? (messages[0].content as InboundData).buttons: undefined; 
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
            :<img className="message-viewer__layout-image"
                  src={chatPicture}
                  alt="Robot"/>
          }
        </div>

        <div className="message-viewer-choice-wrapper">
          {
            choiceList &&
            this.renderChoiceList(choiceList)
          }
        </div>
      </React.Fragment>
    )
  }
}
