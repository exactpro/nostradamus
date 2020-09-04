import React, { Component } from "react";
import cn from "classnames";
import {MessageDataUnion, MessageSendingType, InboundData, OutboundData, InboundChoiceList, InboundReport} from "app/common/store/virtual-assistant/types";
import SelectWindow from "app/modules/settings/elements/select-window/select-window";
import Icon, { IconSize, IconType } from 'app/common/components/icon/icon';
import "app/modules/virtual-assistant/message-viewer/message-viewer.scss";
import chatPicture from "assets/images/chatPicture.png";
import chatbotTypingPreview from "assets/images/chatbotTypingPreview.gif";
import moment from 'moment';
import Button, { ButtonStyled } from "app/common/components/button/button";
import Calendar from 'react-calendar';

interface Props{
  messages: MessageDataUnion[],
  selectMessageData: (item: string, renderItem?: string) => () => void,
}

interface State{
  isChoiceListVisible: boolean,
  dropdownListValues: string[],
  calendarValue: undefined | [Date, Date],
  messagesNumber: number,
  messagesRenderedNumber: number;
}

export default class MessageViewer extends Component<Props, State>{

  state:State={
    isChoiceListVisible: true,
    dropdownListValues: [],
    calendarValue: undefined,
    messagesNumber: 0,
    messagesRenderedNumber: 0
  }

  dateRestriction = {
		minDateValue: new Date(0),
		maxDateValue: new Date(),
  }

  calendarRef: React.RefObject<HTMLDivElement> = React.createRef();
  timerID: NodeJS.Timeout | undefined = undefined;

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

  renderChoiceList = (choiceList: InboundChoiceList[]) => (
    <div className={cn("message-viewer-choice-list",{"message-viewer-choice-list_hidden": !this.state.isChoiceListVisible})}>
      {
        choiceList.map((item,index)=>(
          <button key={index} className="message-viewer-choice-list__item"
                  onClick={this.selectMessageData(item.title)}>
            {item.title}
          </button>
        ))}
    </div>)

  renderUploadFile = ({filename, format, link, size, filters}: InboundReport, index: number) => (
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
          
          <div className={"message-viewer-file-upload__info-title"}>
            <p>{size}</p>
            <p>{format}</p>
          </div>

          {
            (filters && filters.project) &&
            <div className={"message-viewer-file-upload__info-filters"}>
              <p>{filters.project.join(", ")}</p>
            </div>
          }
      
        </div>
      </div>
    </div>
  )

  renderCalendar = (calendarTitle: string) => (
        <div className={cn("message-viewer-calendar",
                           "message-viewer-message",
                           `message-viewer-message_${MessageSendingType.inbound}`)}>
          <p className="message-viewer-calendar__title">{calendarTitle}</p>

          <div className="message-viewer-calendar__calendar"
               ref={this.calendarRef}>
            <Calendar locale="en-EN"
                      minDate={this.dateRestriction.minDateValue}
							        maxDate={undefined/*this.dateRestriction.maxDateValue*/}
                      onClickDay={this.setCalendarDate}
                      onChange={this.setCalendarDate}
                      returnValue = "range"
                      selectRange={true}
                      showNeighboringMonth={false}
                      formatShortWeekday={(_: any, date: Date) => ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'St'][date.getDay()]}
                      />
          </div>

          <div className={cn("message-viewer-widget-buttons", "message-viewer-widget-buttons_calendar")}>
            <Button text="Send Date"
                    onClick={this.selectCalendarData}
                    styled={ButtonStyled.Flat}
                    type="submit"
                    className={cn("message-viewer-widget-buttons__send")}/>
          </div>

        </div>
        )

  renderDropdownList = (dropdownList: string[]) => (
    <div className="message-viewer-dropdown-list">
          <SelectWindow selectWindowAllValues={dropdownList}
                        selectWindowCheckedValues={this.state.dropdownListValues}
                        searchable={true}
                        placeholder="Select a project"
                        onSelectValue={this.selectDropdownListValue}>
                          <div className="message-viewer-widget-buttons">
                            <Button className={cn("message-viewer-widget-buttons__send",
                                                  {"message-viewer-widget-buttons__send_disabled": !this.state.dropdownListValues.length})}
                                    text="Send Selected"
                                    styled={ButtonStyled.Flat}
                                    type="submit"
                                    onClick={this.selectDropdownListData}
                                    disabled={!this.state.dropdownListValues.length}/>
                          </div>
          </SelectWindow>
        </div>
  )

  shouldComponentUpdate = (nextProps: Props) => {
    if(!this.state.isChoiceListVisible && this.props.messages.length !== nextProps.messages.length) this.setState({isChoiceListVisible:true});
    if(nextProps.messages.length !== this.props.messages.length) this.setState({messagesNumber: nextProps.messages.length}, ()=> this.state.messagesRenderedNumber !== this.state.messagesNumber && this.startQueueMessagesRendering());
    return true;
  }

  componentDidUpdate = (prevProps: Props) => {
    if(this.calendarRef.current){
      let prevButton = this.calendarRef.current.getElementsByClassName("react-calendar__navigation__prev-button");
      let nextButton = this.calendarRef.current.getElementsByClassName("react-calendar__navigation__next-button");
      
      if(!prevButton || !nextButton) return;

      prevButton[0].classList.add('icon','icon-Left-Arrow');
      nextButton[0].classList.add('icon','icon-Left-Arrow', 'icon-Left-Arrow__next');

      prevButton[0].innerHTML = "";
      nextButton[0].innerHTML = "";
    }

  }

  clearInterval = () => { 
      clearInterval(this.timerID as NodeJS.Timeout);
      this.timerID = undefined; 
  }

  startQueueMessagesRendering = () => {
    
    if(this.timerID) this.clearInterval();

    if(this.props.messages[this.props.messages.length - 1].messageType === MessageSendingType.outbound) 
      this.setState((prevState)=>({ messagesRenderedNumber: prevState.messagesRenderedNumber + 1, messagesNumber: prevState.messagesNumber + 1 }))

    this.timerID = setInterval(()=>{  
      if(this.state.messagesNumber === this.state.messagesRenderedNumber) this.clearInterval();

      else this.setState((prevState)=>({
        messagesRenderedNumber: prevState.messagesRenderedNumber + 1
      }));
    
    }, 3000)
  
  }

  setCalendarDate = (dateVal: Date | [Date, Date]) => {
    let startDate, endDate;

    if(Array.isArray(dateVal)) [startDate, endDate] = dateVal;
    else {
      startDate = new Date(dateVal.getTime());
      endDate = new Date(dateVal.getTime()); 
    }

    endDate.setHours(23,59,59);
    this.setState({calendarValue: [startDate, endDate]});
  }

  selectDropdownListData = () => {
    this.props.selectMessageData(JSON.stringify(this.state.dropdownListValues), this.state.dropdownListValues.join(", "))();
    this.setState({dropdownListValues: []});
  }

  selectCalendarData = () => { 
    if(!this.state.calendarValue) return;

    let [startDate, endDate] = this.state.calendarValue;
    let dateSendMessage: string = JSON.stringify(this.state.calendarValue); 
    let dateRenderMessage: string;

    if(moment(startDate).isSame(endDate, "day")) dateRenderMessage = moment(startDate).format("DD.MM.YYYY");
    else dateRenderMessage = `${moment(startDate).format("DD.MM.YYYY")} - ${moment(endDate).format("DD.MM.YYYY")}`;
    
    this.props.selectMessageData(dateSendMessage, dateRenderMessage)();
    this.setState({calendarValue: undefined});
  }

  selectMessageData = (message: string) => () => {
    this.setState({ isChoiceListVisible: false });
    setTimeout(this.props.selectMessageData(message), 200);
  }

  selectDropdownListValue = (value: string, isChecked: boolean) => () => {
    let {dropdownListValues} = this.state;

    if(isChecked) dropdownListValues = dropdownListValues.filter(item=>item!==value);
    else dropdownListValues.push(value);

    this.setState({dropdownListValues});
  }

  render(){
    let messages = this.props.messages.slice(0, this.state.messagesRenderedNumber).reverse(); 

    let choiceList;
    let dropdownList;
    let calendarTitle: string|undefined;

    if(messages[0]){
      choiceList = (messages[0].content as InboundData).buttons;
      if((messages[0].content as InboundData).custom?.operation==="calendar") calendarTitle = (messages[0].content as InboundData).custom?.title;
      if((messages[0].content as InboundData).custom?.operation==="filtration") dropdownList = (messages[0].content as InboundData).custom?.values;
    }
    
    return(
      <React.Fragment>
        <div className="message-viewer">
          {
            calendarTitle &&
            this.renderCalendar(calendarTitle)
          }

          {
            dropdownList &&
            this.renderDropdownList(dropdownList)
          }

          {
            messages.length?
            messages.map((item: MessageDataUnion , index: number)=>{ 
              let report: InboundReport|undefined = (item.content as InboundData).custom;
              if(report?.operation === "report") return this.renderUploadFile(report, index);
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
