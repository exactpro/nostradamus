export enum MessageSendingType{
  outbound = "outbound",
  inbound = "inbound",
}
export interface MessageItem{
  type: MessageSendingType,
  //isRead: boolean,
  //date: Date,
  message: string| string[],
}

export enum VirtualAssistantActionTypes{
    activateVirtualAssistant = "ACTIVATE_VIRTUAL_ASSISTANT",
    activateMessage = "ACTIVATE_MESSAGE",
}

export interface VirtualAssistantStore{
  [key: string]: boolean|Array<MessageDataUnion>,
  isOpen: boolean,
  messages: Array<MessageDataUnion>,
}

export interface OutboundData{
  sender: string,
  message: string,
}

export interface InboundData{
  recipient_id: string,
  text?: string,
  buttons?: InboundChoiceList[],
  custom?: InboundReport,
}

export type InboundChoiceList = {
  payload: string,
  title: string
}

export type InboundReport = {
  filename: string,
  format:  string,
  link:  string,
  size:  string,
}

export type MessageDataUnion = {
  messageType: MessageSendingType,
  content: InboundData | OutboundData,
}
