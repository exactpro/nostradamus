import React, { Component } from "react";
import {MessageDataUnion, MessageSendingType, InboundData, InboundReport, InboundChoiceList} from "app/common/store/virtual-assistant/types";
import "app/modules/virtual-assistant/message-viewer/message-viewer.scss";
import chatPicture from "assets/images/chatPicture.png";
import chatbotTypingPreview from "assets/images/chatbotTypingPreview.gif";
import MessageViewerCalendar from "./message-viewer-render-function/message-viewer-calendar";
import MessageViewerDropdownList from "./message-viewer-render-function/message-viewer-dropdown-list";
import MessageViewerFileUpload from "./message-viewer-render-function/message-viewer-file-upload";
import MessageViewerChoiceList from "./message-viewer-render-function/message-viewer-choice-list";
import MessageViewerMessage from "./message-viewer-render-function/message-viewer-message";

interface Props{
  messages: MessageDataUnion[],
  selectMessageData: (item: string, renderItem?: string) => () => void,
}

interface State{
  messagesNumber: number,
  messagesRenderedNumber: number;
}

export default class MessageViewer extends Component<Props, State>{

  state:State={
    messagesNumber: 0,
    messagesRenderedNumber: 0
  }
  
  timerID: NodeJS.Timeout | undefined = undefined;

  shouldComponentUpdate = (nextProps: Props) => {
    if(nextProps.messages.length !== this.props.messages.length) this.setState({messagesNumber: nextProps.messages.length}, ()=> this.state.messagesRenderedNumber !== this.state.messagesNumber && this.startQueueMessagesRendering());
    return true;
  }

  clearQueueMessagesRenderingInterval = () => { 
      clearInterval(this.timerID as NodeJS.Timeout);
      this.timerID = undefined; 
  }

  startQueueMessagesRendering = () => {
    
    if(this.timerID) this.clearQueueMessagesRenderingInterval();

    if(this.props.messages[this.props.messages.length - 1].messageType === MessageSendingType.outbound) 
      this.setState((prevState)=>({ messagesRenderedNumber: prevState.messagesRenderedNumber + 1, messagesNumber: prevState.messagesNumber + 1 }))

    this.timerID = setInterval(()=>{  
      if(this.state.messagesNumber === this.state.messagesRenderedNumber) this.clearQueueMessagesRenderingInterval();

      else this.setState((prevState)=>({
        messagesRenderedNumber: prevState.messagesRenderedNumber + 1
      }));
    
    }, 3000)
  
  }

  render(){
    let messages: MessageDataUnion[] = this.props.messages.slice(0, this.state.messagesRenderedNumber).reverse(); 

    let choiceList: InboundChoiceList[] | undefined;
    let dropdownValues: string[] | undefined;
    let calendarTitle: string | undefined;

    if(messages[0]){
      choiceList = (messages[0].content as InboundData).buttons;
      if((messages[0].content as InboundData).custom?.operation==="calendar") calendarTitle = (messages[0].content as InboundData).custom?.title;
      if((messages[0].content as InboundData).custom?.operation==="filtration") dropdownValues = (messages[0].content as InboundData).custom?.values;
    }
    
    return(
      <React.Fragment>
        <div className="message-viewer">
          {
            calendarTitle &&
            <MessageViewerCalendar calendarTitle={calendarTitle}
                                   sendCalendarDate={this.props.selectMessageData}/>
          }

          {
            dropdownValues &&
            <MessageViewerDropdownList allDropdownValues={dropdownValues}
                                       sendDropdownListData={this.props.selectMessageData}/>
          }

          {
            messages.length?
            messages.map((item: MessageDataUnion , index: number)=>{ 
              let report: InboundReport|undefined = (item.content as InboundData).custom;
              if(report?.operation === "report") return <MessageViewerFileUpload key={index} report={report}/>;
              return <MessageViewerMessage key={index} messageItem={item}/>
            })
            :<img className="message-viewer__layout-image"
                  src={chatPicture}
                  alt="Robot"/>
          }
        </div>

        <div className="message-viewer-choice-wrapper">
          {
            choiceList &&
            <MessageViewerChoiceList choiceList={choiceList}
                                     sendMessageData={this.props.selectMessageData}/>
          }
        </div>
        
        {
          this.state.messagesRenderedNumber !== this.state.messagesNumber &&
          <div className="message-viewer-typing-preview">
              <p className="message-viewer-typing-preview__title">Nostradamus is typing</p>
              <img className="message-viewer-typing-preview__image" src={chatbotTypingPreview} alt="Chatbot typing preview"/>
          </div>
        }
        
      </React.Fragment>
    )
  }
}
