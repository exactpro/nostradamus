
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

export enum VirtualAssistantActionTypes {
  activateVirtualAssistant = "ACTIVATE_VIRTUAL_ASSISTANT",
  activateMessage = "ACTIVATE_MESSAGE",
  clearMessages = "CLEAR_MESSAGES"
}

export interface VirtualAssistantStore{
  [key: string]: boolean|Array<MessageDataUnion>,
  isOpen: boolean,
  messages: Array<MessageDataUnion>,
}

export interface OutboundData{
  sender: string | number,
  message: string,
}

export type InboundData = {
  [key: string]: undefined | string | string[] | boolean | InboundChoiceList[] | InboundReport,
  recipient_id: string,
  text?: string,
  buttons?: InboundChoiceList[],
  custom?: InboundReport,
  calendar?: boolean,
  filters?: string[]
}

export type InboundChoiceList = {
  payload: string,
  title: string
}

export type InboundReport = {
  operation?: string,
  values?: string[],
  filename?: string,
  format?:  string,
  link?:  string,
  size?:  string,
  title?: string
  filters?: {
    period?: string[],
    project?: string[]
  }
}

export type MessageDataUnion = {
  messageType: MessageSendingType,
  content: InboundData | OutboundData,
}
